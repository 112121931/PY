# prompt: 1A1B的遊戲, 
# 由使用者輸入一個四位的數字, 若未輸入, 由程式自動產生不重複的4碼數字
# 透過以下程序來猜答案, 
# 1.先將四位數字, 分別設定為獨立的LIST, 內容為0~9
# 2.猜測一個數字
#  A.由相對的位置中, 選擇目前LIST裡的內容, 組成猜測的數字, 數字不可重覆
#  B.猜測的數字不可與之前重複
#  C.每一次的猜測, 都需符合前面的猜測結果
#  D.不能符合前幾項要求時, 重新產生新的數字
# 3.如果結果A=0 And B != 0,  將對應位置的LIST中, 將目前猜測的數字移除,  
# 4.如果結果A != 0 And B=0,  保留對應位置的數值, 於另外三個LIST中, 將猜測的數字移除,  
# 5.若結果為A=0 And B=0, 將目前猜測的數值, 於四個LIST中移除, 
# 6.若A+B的結果為4, 則將不是目前的四個數字, 由目前的陣列中移除,
# 7.回到猜測數字的流程
# 8.猜測10還猜不到, 就放棄

import random
import sys

def generate_guess(possible_digits):
  """
 2.猜測一個數字
  A.由相對的位置中, 選擇目前LIST裡的內容, 組成猜測的數字, 數字不可重覆
  B.猜測的數字不可與之前重複

  Args:
    possible_digits: 一個包含四個數字列表的列表，每個列表包含可能的數字。

  Returns:
    一個四位數的猜測。
  """
  guess = []
  for i in range(4):
    # 隨機選擇一個數字
    if len(possible_digits[i]) == 0:
      print(f"無解喔!!! 第{i+1}個數字已無解")
      sys.exit()

    digit = random.choice(possible_digits[i])
    while(digit in guess) :
      dupflag = True
      for item in possible_digits[i]:
        if item not in guess:
          dupflag = False
          break;
      
      if dupflag == True:
        return None
      
      digit = random.choice(possible_digits[i])
    guess.append(digit)

  return guess

def get_feedback(guess, secret_number):
  """
  取得猜測結果的回饋。

  Args:
    guess: 猜測的數字。
    secret_number: 正確的數字。

  Returns:
    一個包含 A 和 B 數量的元組。
  """
  a_count = 0
  b_count = 0
  for i in range(4):
    if guess[i] == secret_number[i]:
      a_count += 1
    elif guess[i] in secret_number:
      b_count += 1
  return a_count, b_count

def check_guess(guess, guessed):
  '''
  將這次猜測的的數字, 與先前猜測的數字進行驗證, 去除不合理的猜測
  '''    
  if guessed is None:
    return True
  
  if guess is None:
    return False

  #猜測的數字不可重覆
  for item in guessed:
    if guess == item[0]:
      return False
    
    #  C.每一次的猜測, 都需符合前面的猜測結果  
    a_count, b_count = get_feedback(guess, item[0])
    if a_count != item[1] or b_count != item[2]:
      return False

def get_secretnumber():
  '''
  隨機產生四碼不重複數字
  '''      
  secret_number = [random.randint(0, 9) for _ in range(4)]
  while secret_number[0] == secret_number[1] or \
        secret_number[0] == secret_number[2] or \
        secret_number[0] == secret_number[3] or \
        secret_number[1] == secret_number[2] or \
        secret_number[1] == secret_number[3] or \
        secret_number[2] == secret_number[3]:
    secret_number = [random.randint(0, 9) for _ in range(4)]
  return secret_number
          
def play_game():
  """
  玩 1A1B 遊戲。
  """
  # 初始化可能的數字列表
  possible_digits = [[i for i in range(10)] for _ in range(4)]
  # 設定秘密數字
  print("請輸入四位不重複數字，自動展示推演過程")
  print("也可不輸入，由您來回答我每一次的結果")
  secret_string = input("請輸入：")
  secret_number= []
  if secret_string != "":
    secret_number = [int(x) for x in str(secret_string).zfill(4)]

  # 開始猜測
  guessed = []
  # 8.猜測10還猜不到, 就放棄
  for i in range(10):
    # 生成猜測
    guess = generate_guess(possible_digits)
    checkcount = 0
    while check_guess(guess, guessed) == False: #不能符合前幾項要求時, 重新產生新的數字
      checkcount += 1
      if checkcount == 1000:
        print(f"您提供的答案似乎有誤，我覺得可能無解")
        break;
      guess = generate_guess(possible_digits)
      
    print(f"猜測: {''.join(str(x) for x in guess)}")
    # 取得回饋
    a_count = 0
    b_count = 0
    if secret_string != "":
        a_count, b_count = get_feedback(guess, secret_number)
    else:
      a_count = int(input("請輸入A的數量："))
      b_count = int(input("請輸入B的數量："))
    print(f"結果: {a_count}A{b_count}B")

    # 根據回饋更新可能的數字列表
    if a_count == 0 and b_count == 0:
      #目前的四個數字都不可能
      for j in range(4):
        if guess[j] in possible_digits[j]:
          possible_digits[j].remove(guess[j])
    elif a_count == 0 and b_count != 0:
      #目前的數字都不可能出現在目前的位置
      for j in range(4):
        if guess[j] in possible_digits[j]:
          possible_digits[j].remove(guess[j])
    elif a_count != 0 and b_count == 0:
      #目前的數字都只可能出現在目前的位置
      for k in range(4):
        for j in range(4):
            if j != k and guess[k] in possible_digits[j]:
                possible_digits[j].remove(guess[k])
    
    if a_count + b_count == 4:
      #不可能有其它的數值
      for k in range(4):
        temp = []
        for item in possible_digits[k]:
          if item in guess:
            temp.append(item)
        possible_digits[k] = temp

    """
    print(possible_digits[0])
    print(possible_digits[1])
    print(possible_digits[2])
    print(possible_digits[3])
    """
    # 檢查是否猜對
    if a_count == 4:
      print(f"我用{i+1}次猜對囉！")
      break
    else :      
      guessed.append([guess, a_count, b_count])

  if a_count != 4:
    print(f"很抱歉，我猜不到答案。")
    answer_str = input("請問答案是：")
    answer = [int(x) for x in str(answer_str).zfill(4)]
    for item in guessed:
      a_count, b_count = get_feedback(item[0], answer)
      if (a_count != item[1] or b_count != item[2]):
        print(f"你在 {item[0]} 時，回答的結果有誤喔!!我哪猜的出來啊!!")

def main():
  # 啟動遊戲
  play_game()

if __name__ == "__main__":
  main()