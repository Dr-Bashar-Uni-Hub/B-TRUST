# Deviations log (empty at registration)

## D1 (logged before running Phase 61)
Prereg E2 says "integrate loss over coverage by trapezoid on realised (U, risk) points with U>0" but does not state whether
the two methods are integrated over a common coverage range. An unnormalised integral favours the method with a narrower
realised range. Resolution (conservative): report BOTH (a) literal unnormalised AURC_w and (b) mean risk over the common
range [max(minU_HIER, minU_FLAT), 1]. H2 is declared supported only if BOTH CIs exclude 0 in favour of HIER.

## D2 (logged after Phase 63 run, before any re-analysis)
Implementation flaw found in my Phase 63 fixed-sequence procedure: the first (most conservative) lambda on each path accepts
no calibration items, so the video-mean test statistic is exactly 0, p = 1, and the sequence halts immediately. The 0/12 result
is therefore partly an artefact. Diagnostic (not a replacement result): compute, for every seed, the minimum p-value over the
entire grid (i.e., the most favourable single lambda, which is optimistic because it ignores multiplicity). If no lambda
reaches p <= delta even optimistically, the conclusion "no certifiable policy" does not depend on the flaw.
