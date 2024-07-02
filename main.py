import pygame
import sys
import io
import contextlib
import os
import threading

pygame.init()
pygame.display.set_caption("Python Editor")
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font("simkai.ttf", 25)
code = ""
output = ""

# 按钮属性
button_rect = pygame.Rect(600, 500, 150, 50)
button_color = (0, 255, 0)
button_text = font.render("运行", True, (0, 0, 0))
# 保存和打开按钮属性
save_button_rect = pygame.Rect(420, 500, 150, 50)
save_button_color = (0, 0, 255)
save_button_text = font.render("保存", True, (255, 255, 255))

open_button_rect = pygame.Rect(240, 500, 150, 50)
open_button_color = (255, 0, 0)
open_button_text = font.render("打开文件", True, (255, 255, 255))
# 代码补齐字典
code_completion_dict = {
    "def": "def function_name(parameters):\n\tpass",
    "if": "if condition:\n\tpass",
    "for": "for item in iterable:\n\tpass",
    "while": "while condition:\n\tpass",
    "class": "class ClassName:\n\tdef __init__(self, parameters):\n\t\tpass"
}

# 代码高亮颜色
KEYWORD_COLOR = (0, 0, 255)
STRING_COLOR = (0, 128, 0)
NUMBER_COLOR = (128, 0, 128)
COMMENT_COLOR = (128, 128, 128)

# 关键字列表
KEYWORDS = ["print","input","def", "if", "for", "while", "class", "pass", "return", "in", "not", "and", "or", "True", "False", "None"]

def run_code():
    global output
    output = ""  # 清空上一条报错信息
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    try:
        exec(code)
    except Exception as e:
        output += f"\nError: {str(e)}"
    finally:
        sys.stdout = old_stdout
        output += redirected_output.getvalue()

def save_file():
    with open("code.py", "w", encoding='utf-8') as file:
        file.write(code)

def open_file():
    global code
    try:
        with open("code.py", "r", encoding='utf-8') as file:
            code = file.read()
    except FileNotFoundError:
        code = ""

def complete_code(current_line):
    for keyword, snippet in code_completion_dict.items():
        if current_line.strip().startswith(keyword):
            return snippet
    return current_line

def highlight_code(line):
    words = line.split()
    highlighted_line = []
    for word in words:
        if word in KEYWORDS:
            highlighted_line.append((word, KEYWORD_COLOR))
        elif word.startswith('"') and word.endswith('"') or word.startswith("'") and word.endswith("'"):
            highlighted_line.append((word, STRING_COLOR))
        elif word.isdigit():
            highlighted_line.append((word, NUMBER_COLOR))
        elif word.startswith('#'):
            highlighted_line.append((word, COMMENT_COLOR))
        else:
            highlighted_line.append((word, (0, 0, 0)))
    return highlighted_line

def input_thread():
    global output
    try:
        user_input = input()
        output += f"\n{user_input}"
    except EOFError:
        pass

if __name__ == '__main__':
    while True:
        screen.fill((255, 255, 255))

        # 绘制代码编辑区
        pygame.draw.rect(screen, (200, 200, 255), (40, 40, 720, 200))  # 代码编辑区背景颜色
        lines = code.split('\n')
        y = 50
        for i, line in enumerate(lines):
            highlighted_line = highlight_code(line)
            x = 50
            for word, color in highlighted_line:
                text = font.render(word, True, color)
                screen.blit(text, (x, y))
                x += text.get_width() + 5
            y += 40

        # 绘制终端执行区
        pygame.draw.rect(screen, (255, 200, 200), (40, 290, 720, 200))  # 终端执行区背景颜色
        output_lines = output.split('\n')
        y = 300
        for line in output_lines:
            text = font.render(line, True, (0, 0, 0))
            screen.blit(text, (50, y))
            y += 40

        # 绘制按钮
        pygame.draw.rect(screen, button_color, button_rect)
        screen.blit(button_text, (button_rect.x + 20, button_rect.y + 10))

        pygame.draw.rect(screen, save_button_color, save_button_rect)
        screen.blit(save_button_text, (save_button_rect.x + 20, save_button_rect.y + 10))

        pygame.draw.rect(screen, open_button_color, open_button_rect)
        screen.blit(open_button_text, (open_button_rect.x + 20, open_button_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    code = code[:-1]  # 删除最后一个字符
                elif event.key == pygame.K_RETURN:
                    code += '\n'  # 添加换行符
                elif event.key == pygame.K_TAB:
                    code += "    "
                else:
                    code += event.unicode  # 添加按键字符
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    threading.Thread(target=run_code).start()
                if save_button_rect.collidepoint(event.pos):
                    threading.Thread(target=save_file).start()
                if open_button_rect.collidepoint(event.pos):
                    threading.Thread(target=open_file).start()

        pygame.display.update()
