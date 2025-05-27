# -----------------------------------------------------------------------------
# MIT License
# 
# Copyright (c) 2025 Amine Bouzaid
# Creator GitHub: https://github.com/ZapBot-dev 
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----------------------------------------------------------------------------



from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
load_dotenv()
limit = os.getenv("USER_LIMIT_REQUESTS")
def is_allowed_to_use(user_data, limit=int(limit), block_hours=24):
    now = datetime.now()

    # تحقق من الحظر
    if "blocked_until" in user_data:
        if now < user_data["blocked_until"]:
            return False, f"❌ You are blocked until {user_data['blocked_until'].strftime('%Y-%m-%d %H:%M:%S')}."
        else:
            # رفع الحظر بعد انتهاء المدة
            user_data.pop("blocked_until")
            user_data["count"] = 0
            user_data["start_time"] = now

    # أول مرة يستخدم
    if "start_time" not in user_data:
        user_data["start_time"] = now
        user_data["count"] = 0

    # إعادة التهيئة بعد 24 ساعة
    if now - user_data["start_time"] > timedelta(hours=24):
        user_data["start_time"] = now
        user_data["count"] = 0

    # التحقق من الحد
    if user_data["count"] < limit:
        user_data["count"] += 1
        return True, None
    else:
        user_data["blocked_until"] = now + timedelta(hours=block_hours)
        return False, f"🚫 You've reached your daily limit of {limit} requests. Try again after 24 hours."
