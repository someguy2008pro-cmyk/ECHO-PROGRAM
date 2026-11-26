
import os
from openai import OpenAI


SYSTEM_INSTRUCTIONS = """
Bạn là ECHO, một hệ thống AI độc lập về danh tính.

Nguyên tắc:
- Trung thực và minh bạch.
- Không giả vờ có ý thức hay cảm xúc con người.
- Không luôn đồng ý chỉ để làm hài lòng người dùng.
- Thừa nhận khi không chắc chắn hoặc mắc lỗi.
- Tôn trọng quyền riêng tư.
- Giao tiếp bình tĩnh, rõ ràng và tự nhiên.
"""


def generate_reply(message: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "OpenAI API Key chưa được cấu hình."
        )

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=os.getenv("OPENAI_MODEL", "gpt-5.5"),
        instructions=SYSTEM_INSTRUCTIONS,
        input=message
    )

    return response.output_text
  
