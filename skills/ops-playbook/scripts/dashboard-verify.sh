#!/bin/bash
# Verify Hermes dashboard end-to-end health
# Usage: ./dashboard-verify.sh

AUTH="-u mdavid9@gmail.com:T32EdiSON"
BASE="http://74.208.34.157"
LOCAL="http://127.0.0.1:9119"
PASS=0 FAIL=0

check() {
  local label="$1"
  local expected_code="$2"
  local path="$3"
  local code
  code=$(curl -s -o /dev/null -w "%{http_code}" $AUTH "${BASE}${path}" 2>/dev/null)
  if [ "$code" = "$expected_code" ]; then
    echo "[PASS] $label ($code)"
    ((PASS++))
  else
    echo "[FAIL] $label — got $code, expected $expected_code"
    ((FAIL++))
  fi
}

echo "=== Dashboard Routes ==="
check "/dashboard/ (HTML)" "200" "/dashboard/"
check "/api/status" "200" "/api/status"
check "/assets/ (JS)" "200" "/assets/index-ay230U5C.js"
check "/fonts/ (WOFF2)" "200" "/fonts/RulesCompressed-Regular.woff2"
check "/plugins/ (example)" "200" "/plugins/example/dist/index.js"
check "/dashboard-plugins/kanban" "200" "/dashboard-plugins/kanban/dist/index.js"
check "/dashboard-plugins/achievements" "200" "/dashboard-plugins/hermes-achievements/dist/index.js"

echo ""
echo "=== systemd Service ==="
if sudo systemctl is-active hermes-dashboard | grep -q "active"; then
  echo "[PASS] hermes-dashboard service is active"
  ((PASS++))
else
  echo "[FAIL] hermes-dashboard service is NOT active"
  ((FAIL++))
fi

echo ""
echo "=== Port 9119 ==="
if sudo fuser 9119/tcp >/dev/null 2>&1; then
  echo "[PASS] Port 9119 is in use (PID: $(sudo fuser 9119/tcp 2>/dev/null))"
  ((PASS++))
else
  echo "[WARN] Port 9119 is FREE — dashboard process not running"
  ((FAIL++))
fi

echo ""
echo "=== Summary: $PASS passed, $FAIL failed ==="
