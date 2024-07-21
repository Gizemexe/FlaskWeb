def normalize_phone_number(phone):
    # Telefon numarasındaki gereksiz karakterleri temizle
    phone = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

    # Eğer telefon numarası +90 ile başlamıyorsa, başına +90 ekle
    if not phone.startswith('+90'):
        phone = '+90' + phone

    # Eğer telefon numarası +90 ile başlayıp ama ikinci bir +90 içeriyorsa, temizle
    phone = phone.replace('+90+90', '+90')

    return phone
