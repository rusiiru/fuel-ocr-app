import easyocr, numpy as np, cv2
reader = easyocr.Reader(['en'])

def extract_numbers_from_bytes(data: bytes) -> dict:
    nparr = np.frombuffer(data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    texts = reader.readtext(gray, detail=0)
    nums = []
    for t in texts:
        t_clean = t.replace(',', '.')
        try: nums.append(float(t_clean))
        except: pass
    if len(nums) < 4: return {}
    nums_sorted = sorted(nums)
    return {"left": nums_sorted[0], "ctr": nums_sorted[1], "right": nums_sorted[2], "pre": nums_sorted[-1]}

def calc_fuel(pre, left, ctr, right):
    fuel = pre - (left + ctr + right)
    required = fuel * 1000
    final = required / 0.78
    return {"fuel": round(fuel,2), "required": round(required,2), "final": round(final,2)}
