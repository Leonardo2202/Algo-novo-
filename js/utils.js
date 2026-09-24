window.AN_UTIL = {
  money(v) {
    return '€' + v.toFixed(2).replace('.', ',');
  },

  wa(phone, text) {
    const digits = String(phone).replace(/[^0-9]/g, '');
    return 'https://wa.me/' + digits + (text ? '?text=' + encodeURIComponent(text) : '');
  }
};
