import fugashi
import romkan

# 创建Tagger对象
tagger = fugashi.Tagger()

def add_furigana(text):
    words = tagger(text)
    result = ""
    
    for word in words:
        # 获取词形和假名
        surface = word.surface
        furigana = word.feature.kana
        
        # 如果词形和假名不同（说明是汉字），就标注假名
        if surface != furigana:
            furigana_romanized = romkan.to_hepburn(furigana)
            result += f"{surface}({furigana_romanized})"
        else:
            result += surface
    
    return result

# 测试例子
text = "私は学生です。東京に住んでいます。"
print(add_furigana(text))

