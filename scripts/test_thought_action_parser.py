import re

def parse_thought_action(text):
    """
    解析文本中的思考和动作部分。
    
    参数:
        text (str): 包含思考和代码块的文本
        
    返回:
        tuple: (思考部分, 动作部分)
        
    异常:
        ValueError: 如果没有找到有效的代码块
    """
    # 调试信息
    print("输入文本:")
    print("-" * 50)
    print(text)
    print("-" * 50)
    
    # 匹配代码块的开始和结束
    code_block_pat = re.compile(r"^```(\S*)\s*\n|^```\s*$", re.MULTILINE)
    
    # 打印所有匹配
    print("\n所有匹配:")
    for i, match in enumerate(code_block_pat.finditer(text)):
        print(f"匹配 {i+1}: 位置 {match.start()}-{match.end()}, 组1: '{match.group(1)}'")
    
    # 重置迭代器
    stack = []
    last_valid_block = None
    
    print("\n解析过程:")
    for i, match in enumerate(code_block_pat.finditer(text)):
        print(f"\n处理匹配 {i+1}:")
        if stack and not match.group(1):  # 代码块结束
            start = stack.pop()
            print(f"  发现结束标记，弹出栈顶元素 (位置 {start.start()})")
            print(f"  当前栈深度: {len(stack)}")
            # 检查是否不是嵌套在另一个块中
            if not stack:
                last_valid_block = (start, match)
                print(f"  栈为空，记录有效块: ({start.start()}, {match.end()})")
            else:
                print("  栈不为空，这是嵌套块的结束")
        elif match.group(1) is not None:  # 代码块开始
            stack.append(match)
            print(f"  发现开始标记，压入栈 (位置 {match.start()})")
            print(f"  当前栈深度: {len(stack)}")
    
    print("\n最终结果:")
    if last_valid_block:
        start, end = last_valid_block
        thought = text[: start.start()] + text[end.end() :]
        action = text[start.end() : end.start()]
        
        print(f"找到最后一个有效块: ({start.start()}, {end.end()})")
        print(f"思考部分长度: {len(thought)}")
        print(f"动作部分长度: {len(action)}")
        
        return thought, action
    else:
        print("没有找到有效的代码块")
        raise ValueError("No action found in text.")

# 测试用例1: 普通代码块
test_case_1 = f"""
Parses the action from the output of the API call.
We assume that the action is the last code block in the model_response.
We also assume that the action is not nested within another code block.
This is problematic if the model_response includes many unnamed 
For instance:
```python
python3 main.py
```
```bash
ls -l
```
"""

parse_thought_action(test_case_1)