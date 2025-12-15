from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bmi-secret-key-2025'

def calculate_bmi(weight, height):
    """計算 BMI 值"""
    return weight / (height ** 2)

def get_bmi_category(bmi):
    """根據 BMI 值返回分類與健康建議"""
    if bmi < 18.5:
        return {
            'category': '體重過輕',
            'color': 'info',
            'advice': '建議增加營養攝取，加強運動鍛煉，定期體檢。'
        }
    elif 18.5 <= bmi < 24.9:
        return {
            'category': '正常體重',
            'color': 'success',
            'advice': '保持健康的生活習慣，定期運動，均衡飲食。'
        }
    elif 24.9 <= bmi < 29.9:
        return {
            'category': '體重過重',
            'color': 'warning',
            'advice': '建議增加運動量，控制飲食熱量，定期檢測體重。'
        }
    else:
        return {
            'category': '肥胖',
            'color': 'danger',
            'advice': '建議諮詢醫生或營養師，制定合理的減重計畫。'
        }

@app.route('/')
def index():
    """主頁"""
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """計算 BMI 的 API 端點"""
    try:
        data = request.get_json()
        weight = float(data.get('weight'))
        height = float(data.get('height'))
        
        if weight <= 0 or height <= 0:
            return jsonify({'error': '體重和身高必須為正數'}), 400
        
        bmi = calculate_bmi(weight, height)
        category_info = get_bmi_category(bmi)
        
        return jsonify({
            'bmi': round(bmi, 2),
            'weight': weight,
            'height': height,
            'category': category_info['category'],
            'color': category_info['color'],
            'advice': category_info['advice']
        })
    except (ValueError, TypeError):
        return jsonify({'error': '請輸入有效的數字'}), 400

if __name__ == '__main__':
    app.run(debug=True)