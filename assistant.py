from gpt4all import GPT4All
model_name = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"
model = GPT4All(model_name=model_name) 

context = """
user: tại sao bầu trời lại màu xanh?
bạn: Bầu trời có màu xanh vì ánh sáng mặt trời khi xuyên qua khí quyển bị tán xạ, trong đó ánh sáng xanh bị tán xạ mạnh hơn các màu khác do có bước sóng ngắn hơn.
user: bạn có thể chuyển câu trả lời trước đó thành tiếng anh được không
"""


with model.chat_session():
    for token in model.generate(context, streaming=True):
        print(token, end='', flush=True)

with model.chat_session():
    while 1:
        text = input("Bạn: ")
        print('AI: ',end='')
        for token in model.generate(text, streaming=True):
            print(token, end='', flush=True)
        print()
