window.AN_DEFINE_COMPONENT = function (DCLogic) {

class Component extends DCLogic {
  state = {
    intro: true,
    cat: 'all',
    cart: {},
    cartOpen: false,
    langOpen: false,
    typed: '',
    lang: 'pt',
    form: {
      nome: '', email: '', desc: '',
      mode: 'padrao',
      sizes: {},
      artName: '', artDataUrl: '', artType: '', artSize: 0, artError: false,
      artFile: null
    }
  };

  componentDidMount() {
    const D = window.AN_DATA;
    const initLang = this.props.defaultLang && window.AN_I18N[this.props.defaultLang]
      ? this.props.defaultLang
      : D.defaultLang;
    this.setState({ lang: initLang });

    const showIntro = this.props.showIntro !== false;
    if (!showIntro) this.setState({ intro: false });
    else this._t1 = setTimeout(() => this.setState({ intro: false }), 3450);

    this._t2 = setTimeout(() => this.startTyping(initLang), showIntro ? 3100 : 500);
    this._t3 = setTimeout(() => this.reveal(), 60);
  }

  componentWillUnmount() {
    [this._t1, this._t2, this._t3, this._t4].forEach(clearTimeout);
    clearInterval(this._iv);
    if (this._io) this._io.disconnect();
  }

  startTyping(lang) {
    clearInterval(this._iv);
    const phrase = window.AN_I18N[lang].typedPhrase;
    let i = 0;
    this.setState({ typed: '' });
    this._iv = setInterval(() => {
      i += 1;
      this.setState({ typed: phrase.slice(0, i) });
      if (i >= phrase.length) clearInterval(this._iv);
    }, 55);
  }

  setLang(lang) {
    this.setState({ langOpen: false });
    if (lang === this.state.lang) return;
    this.setState({ lang });
    this.startTyping(lang);
  }

  reveal() {
    const nodes = document.querySelectorAll('[data-reveal]');
    const show = (el) => { el.style.opacity = '1'; el.style.transform = 'none'; };
    if (!('IntersectionObserver' in window)) { nodes.forEach(show); return; }
    this._io = new IntersectionObserver((entries) => {
      entries.forEach((e) => { if (e.isIntersecting) { show(e.target); this._io.unobserve(e.target); } });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
    nodes.forEach((n) => this._io.observe(n));
    this._t4 = setTimeout(() => nodes.forEach(show), 4000);
  }

  add(id) {
    this.setState((s) => ({ cart: Object.assign({}, s.cart, { [id]: (s.cart[id] || 0) + 1 }), cartOpen: true }));
  }
  bump(id, d) {
    this.setState((s) => {
      const cart = Object.assign({}, s.cart);
      const n = (cart[id] || 0) + d;
      if (n <= 0) delete cart[id]; else cart[id] = n;
      return { cart };
    });
  }
  bumpSize(size, d) {
    const sizes = Object.assign({}, this.state.form.sizes);
    const n = (sizes[size] || 0) + d;
    if (n <= 0) delete sizes[size]; else sizes[size] = n;
    this.state.form.sizes = sizes;
    this.forceUpdate();
  }
  setMode(mode) {
    this.state.form.mode = mode;
    this.forceUpdate();
  }
  handleArt(e) {
    const file = e.target.files && e.target.files[0];
    if (!file) return;
    if (file.size > window.AN_DATA.maxArtBytes) {
      this.state.form.artError = true;
      this.state.form.artName = file.name;
      this.state.form.artSize = file.size;
      this.state.form.artDataUrl = '';
      this.state.form.artFile = null;
      this.forceUpdate();
      return;
    }
    const reader = new FileReader();
    reader.onload = (ev) => {
      this.state.form.artError = false;
      this.state.form.artName = file.name;
      this.state.form.artType = file.type;
      this.state.form.artSize = file.size;
      this.state.form.artDataUrl = ev.target.result;
      this.state.form.artFile = file;
      this.forceUpdate();
    };
    reader.readAsDataURL(file);
  }
  clearArt() {
    this.state.form.artName = '';
    this.state.form.artDataUrl = '';
    this.state.form.artType = '';
    this.state.form.artSize = 0;
    this.state.form.artError = false;
    this.state.form.artFile = null;
    this.forceUpdate();
  }
  async sendCart(text, phone, file) {
    const digits = String(phone).replace(/[^0-9]/g, '');
    const waUrl = 'https://wa.me/' + digits + '?text=' + encodeURIComponent(text);
    if (file && navigator.canShare && navigator.canShare({ files: [file] })) {
      try {
        await navigator.share({ files: [file], text });
        return;
      } catch (err) {
        if (err && err.name === 'AbortError') return;
      }
    }
    if (file) {
      try {
        const a = document.createElement('a');
        a.href = URL.createObjectURL(file);
        a.download = file.name;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(() => URL.revokeObjectURL(a.href), 2000);
      } catch (_) {}
    }
    window.open(waUrl, '_blank', 'noopener');
  }

  renderVals() {
    const D = window.AN_DATA, U = window.AN_UTIL;
    const t = window.AN_I18N[this.state.lang] || window.AN_I18N[D.defaultLang];
    const showPrices = this.props.showPrices !== false;
    const phone = this.props.whatsappNumber || D.defaultPhone;
    const artEmail = D.artEmail;

    const catalog = D.products;

    const f = this.state.form;
    const projectNome = f.nome || '';
    const projectEmail = f.email || '';
    const projectDesc = f.desc || '';
    const hasProject = !!(projectNome || projectEmail || projectDesc);

    const isCustomMode = f.mode === 'personalizado';
    const sizeRows = D.sizes.map((sz) => ({
      label: sz,
      qty: f.sizes[sz] || 0,
      inc: () => this.bumpSize(sz, 1),
      dec: () => this.bumpSize(sz, -1)
    }));
    const activeSizes = D.sizes
      .filter((sz) => (f.sizes[sz] || 0) > 0)
      .map((sz) => (f.sizes[sz]) + '× ' + sz);
    const customTotal = D.sizes.reduce((a, sz) => a + (f.sizes[sz] || 0), 0);
    const customSizesLabel = activeSizes.join(', ');
    const hasArt = !!f.artDataUrl;
    const noArt = !hasArt;
    const hasCustom = isCustomMode && (customTotal > 0 || hasArt);
    const artSizeLabel = f.artSize ? (f.artSize / 1024 < 1024
      ? (f.artSize / 1024).toFixed(0) + ' KB'
      : (f.artSize / 1024 / 1024).toFixed(2) + ' MB') : '';
    const artSubject = 'Estampa - ' + (projectNome || 'pedido personalizado');
    const artMailto = 'mailto:' + artEmail + '?subject=' + encodeURIComponent(artSubject);

    const lines = Object.keys(this.state.cart).map((id) => {
      const p = catalog.find((x) => x.id === id);
      const info = t.productItems[id];
      if (!p || !info) return null;
      const qty = this.state.cart[id];
      return {
        name: info.name, qty, img: p.img,
        unit: U.money(p.price) + ' ' + t.cart.unit,
        total: U.money(p.price * qty),
        inc: () => this.bump(id, 1), dec: () => this.bump(id, -1),
        sum: p.price * qty
      };
    }).filter(Boolean);
    const count = lines.reduce((a, l) => a + l.qty, 0);
    const total = lines.reduce((a, l) => a + l.sum, 0);

    const parts = [t.wa.greeting];
    if (lines.length) {
      parts.push(t.wa.items + ': ' + lines.map((l) => l.qty + '× ' + l.name).join(', '));
      parts.push(t.wa.total + ': ' + U.money(total));
    }
    if (projectNome)  parts.push(t.wa.nome + ': ' + projectNome);
    if (projectEmail) parts.push(t.wa.email + ': ' + projectEmail);
    if (projectDesc)  parts.push(t.wa.project + ': ' + projectDesc);
    if (hasCustom) {
      parts.push('');
      parts.push('— ' + t.wa.custom + ' —');
      if (customTotal > 0) {
        parts.push(t.wa.sizes + ': ' + customSizesLabel);
        parts.push(t.wa.totalPieces + ': ' + customTotal);
      }
      parts.push(t.wa.art + ': ' + (hasArt ? f.artName : t.wa.noArt));
      parts.push(t.wa.sendArt + ' ' + artEmail);
    }
    const cartText = parts.join('\n');

    return {
      t,
      introVisible: this.state.intro,
      typed: this.state.typed,
      services: t.services.items,
      showPrices,
      phoneLabel: phone,
      waPlain: U.wa(phone, t.wa.contactMsg),
      waCart: U.wa(phone, cartText),

      langOpen: this.state.langOpen,
      toggleLang: () => this.setState((s) => ({ langOpen: !s.langOpen })),
      currentFlag: D.langFlags[this.state.lang],
      currentLangLabel: D.langLabels[this.state.lang],
      langs: D.langCodes.map((code) => {
        const on = this.state.lang === code;
        return {
          label: D.langLabels[code],
          name: (t.langNames && t.langNames[code]) || D.langNames[code],
          flag: D.langFlags[code],
          select: () => this.setLang(code),
          style: Object.assign({}, D.langOptionBase, on ? D.langOptionActive : {})
        };
      }),

      categories: D.categoryOrder.map((key) => {
        const on = this.state.cat === key;
        return {
          label: t.categories[key],
          select: () => this.setState({ cat: key }),
          style: Object.assign({}, D.filterBaseStyle, on ? D.filterActiveStyle : D.filterIdleStyle)
        };
      }),

      visibleProducts: catalog
        .filter((p) => (this.state.cat === 'all' || p.catKey === this.state.cat) && t.productItems[p.id])
        .map((p) => {
          const info = t.productItems[p.id];
          return {
            name: info.name, cat: t.categories[p.catKey], shot: info.shot, img: p.img,
            priceLabel: showPrices ? U.money(p.price) : t.products.quotation,
            add: () => this.add(p.id)
          };
        }),

      cartOpen: this.state.cartOpen,
      openCart: () => this.setState({ cartOpen: true }),
      closeCart: () => this.setState({ cartOpen: false }),
      cartCount: count,
      cartCountLabel: count + ' ' + (count === 1 ? t.cart.piece : t.cart.pieces),
      cartEmpty: lines.length === 0 && !hasProject,
      cartLines: lines,
      cartTotal: showPrices ? U.money(total) : t.products.quotation,

      hasProject,
      projectNome,
      projectEmail,
      projectDesc,

      setNome:  (e) => { this.state.form.nome  = e.target.value; },
      setEmail: (e) => { this.state.form.email = e.target.value; },
      setDesc:  (e) => { this.state.form.desc  = e.target.value; },

      isCustomMode,
      setModePadrao: () => this.setMode('padrao'),
      setModePersonalizado: () => this.setMode('personalizado'),
      modePadraoStyle: Object.assign({}, D.filterBaseStyle, !isCustomMode ? D.filterActiveStyle : D.filterIdleStyle),
      modePersonalizadoStyle: Object.assign({}, D.filterBaseStyle, isCustomMode ? D.filterActiveStyle : D.filterIdleStyle),
      sizeRows,
      customTotal,
      customSizesLabel,
      hasCustom,
      hasArt,
      noArt,
      artPreview: f.artDataUrl,
      artName: f.artName,
      artSizeLabel,
      artError: f.artError,
      artEmail,
      artMailto,
      setArt: (e) => this.handleArt(e),
      clearArt: () => this.clearArt(),
      sendCart: () => this.sendCart(cartText, phone, f.artFile),

      submitForm: (e) => {
        e.preventDefault();
        this.setState({ cartOpen: true });
      }
    };
  }
}

return Component;
};
