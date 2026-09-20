"""제휴 오퍼 슬롯 정의.

애드센스 디스플레이 광고는 노출당 몇 센트지만, 이 사이트 방문자층(62~70세
청구 시점을 계산하는 사람)은 보험·연금·재무상담 리드 바이어가 정확히
찾는 층이다. 같은 트래픽에 단가가 다른 수익원을 붙이는 게 목적이다.

설계 원칙 네 가지 — 바꾸기 전에 이유를 먼저 읽어라:

1. **개인정보를 받지 않는다.** 이 사이트는 정적 호스팅이라 받을 백엔드가
   없고, 미국에서 은퇴·보험 관련 연락처를 받으면 TCPA 동의 요건이 따라온다.
   제휴사 자체 폼으로 보내고, 전환은 그쪽에서 일어난다. 그래서 기존
   개인정보처리방침의 "입력값은 어디로도 전송되지 않는다"가 계속 참이다.

2. **url이 없으면 렌더하지 않는다.** 제휴 가입 전에도 배포할 수 있게,
   빈 슬롯은 HTML에 아예 나오지 않는다. 링크를 채우는 순간 켜진다.

3. **광고임을 표시한다.** 미국은 제휴 링크 고지 의무가 있고, 구글은 유료
   링크에 rel="sponsored"를 요구한다. 둘 다 코드에서 강제한다.

4. **조언처럼 읽히지 않게 쓴다.** about 페이지가 "이 사이트는 청구 시점을
   추천하지 않는다"고 명시했다. 오퍼 문구가 그걸 뒤집으면 안 된다.
   그래서 문구는 '무엇을 비교할 수 있다'까지만 말한다.

연령 창을 이렇게 잡은 근거 (2026-09-20 조사):

  - **하한 55세** — SSA가 만 55세 이상에게 연례 명세서와 함께 "Thinking of
    Retiring?" 안내를 보낸다. 청구 시점을 고민하기 시작하는 제도적 트리거이고,
    이 사이트를 검색으로 찾는 연령대의 실질적 시작점이다.
  - **상한 70세** — 지연 크레딧이 70세에서 멈춘다. 그 뒤로는 '언제 청구할까'라는
    결정 자체가 없어서, 오퍼 문구가 참이 아니게 된다. 리드 가치도 사라진다.
  - **밀도는 60~67세** — 최다 청구 연령은 66세(남 28%, 여 27%), 62세가 20%+,
    70세는 10% 미만. 2019~2023 사이 62세 청구는 줄고 67세 이후가 크게 늘었다.
  - **55세 미만은 오퍼를 띄우지 않는다.** 결정이 임박하지 않아 리드 가치가 낮고,
    계산기를 '먼 미래 계획'으로 써 보는 층이다. 슬롯이 안 맞으면 아무것도
    렌더하지 않으므로 별도 처리가 필요 없다.

이 숫자는 업계 평균이다. **사이트 자체 GA4 데이터가 쌓이면 그걸로 교체해야
한다** — 계산 완료 시 `calc_complete` 이벤트에 연령 버킷을 실어 보내므로,
GA4에서 실제 방문자 연령 분포를 보고 창을 다시 잡을 수 있다.

슬롯을 켜는 법:
  1. 제휴 네트워크에 가입해 이 사이트를 등록한다(사용자가 직접).
  2. 받은 추적 링크를 아래 url에 넣는다.
  3. python build.py -> git push. 끝.
"""

# GA4로 보낼 연령 버킷. 청구 결정 구조에 맞춰 나눴다 -
# 62(최초 청구 가능), 65(메디케어), FRA 66~67, 70(지연 크레딧 종료).
AGE_BUCKETS = [
    (None, 54, "under-55"),
    (55, 59, "55-59"),
    (60, 62, "60-62"),
    (63, 64, "63-64"),
    (65, 67, "65-67"),
    (68, 70, "68-70"),
    (71, None, "71-plus"),
]

# 광고 고지 문구. 모든 오퍼 카드에 붙는다.
DISCLOSURE = ("Advertising disclosure: the link above is a paid partner link. "
              "This site may earn a commission if you request a quote. "
              "It is not a recommendation, and it does not change what the "
              "calculator above shows you.")


class Offer:
    """오퍼 슬롯 하나.

    min_age / max_age: 사용자가 계산한 '현재 나이'가 이 범위일 때만 띄운다.
        None이면 제한 없음. 나이와 무관한 오퍼는 둘 다 비운다.
    """

    def __init__(self, key, headline, body, cta, url=None,
                 min_age=None, max_age=None):
        self.key = key
        self.headline = headline
        self.body = body
        self.cta = cta
        self.url = url
        self.min_age = min_age
        self.max_age = max_age

    @property
    def active(self):
        return bool(self.url)

    def as_js(self):
        return {
            "key": self.key,
            "headline": self.headline,
            "body": self.body,
            "cta": self.cta,
            "url": self.url,
            "minAge": self.min_age,
            "maxAge": self.max_age,
        }


OFFERS = [
    # 메디케어 — 이 사이트와 타이밍이 가장 정확히 맞는 오퍼다. 65세가
    # 메디케어 최초 가입 시기이고, 이 계산기를 쓰는 이유가 바로 그 나이대의
    # 청구 시점 결정이다. 63~67세 구간에만 띄운다.
    Offer(
        key="medicare",
        headline="Turning 65 soon?",
        body="Medicare enrollment has its own deadlines, separate from when you "
             "claim Social Security. Missing the initial window can mean a "
             "permanent premium penalty.",
        cta="Compare Medicare plans",
        url=None,
        # 메디케어 최초 가입 기간은 65세 전후 3개월. 1~2년 앞서 알아보는 층까지 잡는다.
        min_age=63, max_age=67,
    ),
    # 재무상담사 매칭 — 청구 시점 결정은 세금·배우자 급여·다른 소득이 엮여서
    # 계산기가 답할 수 없는 부분이 남는다. 그 지점에 붙인다.
    Offer(
        key="advisor",
        headline="The math above is only part of the decision",
        body="Taxes, a spouse's benefit, and other retirement income can change "
             "which claiming age actually leaves you with more. A licensed "
             "advisor can run your full picture.",
        cta="Find a fiduciary advisor",
        url=None,
        # 55세(SSA 리서치 트리거) ~ 70세(지연 크레딧 종료 = 결정 끝).
        min_age=55, max_age=70,
    ),
    # 연금(애뉴이티) — '늦게 청구하면 그 사이 소득은?' 문제와 직결된다.
    Offer(
        key="annuity",
        headline="Bridging the years before you claim",
        body="If you plan to delay claiming, the gap years still need income. "
             "Annuities and other guaranteed-income products are one option "
             "people compare for that stretch.",
        cta="Compare retirement income options",
        url=None,
        # '청구 전 공백기 소득' 전제라, 70세를 넘기면 공백기가 없어진다.
        min_age=58, max_age=69,
    ),
]


AGE_FLOOR, AGE_CEIL = 0, 120


def _span(offer):
    lo = AGE_FLOOR if offer.min_age is None else offer.min_age
    hi = AGE_CEIL if offer.max_age is None else offer.max_age
    return lo, hi


def active_offers():
    """활성 슬롯을 **창이 좁은 순서로** 돌려준다.

    JS는 조건이 맞는 첫 슬롯을 쓴다. 정의 순서에 맡기면 창이 넓은 슬롯이
    좁은 슬롯을 덮어서 슬롯이 조용히 죽는다 - 실제로 advisor(55~70)가
    annuity(58~69)를 통째로 덮는 걸 발견해서 이 정렬을 넣었다. 창이 좁은 쪽이
    더 구체적인 맥락이니 그쪽이 이기는 게 맞다. 폭이 같으면 정의 순서를 지킨다.
    """
    active = [o for o in OFFERS if o.active]
    return sorted(active, key=lambda o: _span(o)[1] - _span(o)[0])


def unreachable_slots():
    """어떤 나이에도 뜰 수 없는 슬롯. 창을 고칠 때 조용히 죽는 걸 막는 검사다."""
    ordered = active_offers()
    reachable = set()
    for age in range(AGE_FLOOR, AGE_CEIL + 1):
        for o in ordered:
            lo, hi = _span(o)
            if lo <= age <= hi:
                reachable.add(o.key)
                break
    return [o.key for o in ordered if o.key not in reachable]


def coverage(start=50, end=80):
    """나이별로 어느 슬롯이 실제로 뜨는지 구간으로 압축한다."""
    ordered = active_offers()
    out, prev, first = [], "__init__", start
    for age in range(start, end + 1):
        hit = "(없음)"
        for o in ordered:
            lo, hi = _span(o)
            if lo <= age <= hi:
                hit = o.key
                break
        if hit != prev:
            if prev != "__init__":
                out.append((first, age - 1, prev))
            prev, first = hit, age
    out.append((first, end, prev))
    return out


def age_bucket(age):
    for lo, hi, label in AGE_BUCKETS:
        if (lo is None or age >= lo) and (hi is None or age <= hi):
            return label
    return "unknown"


def age_buckets_js():
    import json
    return json.dumps([{"lo": lo, "hi": hi, "label": label}
                       for lo, hi, label in AGE_BUCKETS])


def offers_js_payload():
    """활성 슬롯만 JS로 넘긴다. 비활성 슬롯은 HTML에 흔적이 없다."""
    import json
    return json.dumps([o.as_js() for o in active_offers()], ensure_ascii=False)


def status():
    lines = []
    for o in OFFERS:
        window = ("모든 나이" if o.min_age is None and o.max_age is None
                  else f"{o.min_age or '~'}~{o.max_age or '~'}세".rjust(9))
        state = "✅ 활성" if o.active else "⬜ 링크 없음(렌더 안 됨)"
        lines.append(f"  {state}  [{o.key}] {window} — {o.headline}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(f"제휴 오퍼 슬롯 {len(OFFERS)}개 중 활성 {len(active_offers())}개\n")
    print(status())

    dead = unreachable_slots()
    if dead:
        print()
        print("[막힘] 어떤 나이에도 뜰 수 없는 슬롯: " + ", ".join(dead))
        print("       더 좁은 창의 슬롯이 전 구간을 덮고 있습니다. 창을 조정하세요.")

    if active_offers():
        print()
        print("나이별 실제 노출 (50~80세):")
        for lo, hi, key in coverage():
            span = ("%d세" % lo) if lo == hi else ("%d~%d세" % (lo, hi))
            print("  " + span.rjust(9) + "  ->  " + key)
    if not active_offers():
        print("\n활성 슬롯이 없어 사이트에는 오퍼 영역이 출력되지 않습니다.")
        print("제휴 네트워크 가입 후 offers.py의 url= 에 추적 링크를 넣으세요.")
