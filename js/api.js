(function () {
  const BASE = '';

  async function req(path, opts) {
    opts = opts || {};
    const init = {
      method: opts.method || 'GET',
      credentials: 'include',
      headers: opts.headers || {}
    };
    if (opts.body !== undefined) {
      if (opts.body instanceof FormData) {
        init.body = opts.body;
      } else {
        init.headers['Content-Type'] = 'application/json';
        init.body = JSON.stringify(opts.body);
      }
    }
    const res = await fetch(BASE + path, init);
    let data = null;
    const ct = res.headers.get('content-type') || '';
    if (ct.includes('application/json')) {
      try { data = await res.json(); } catch (_) {}
    }
    if (!res.ok) {
      const err = new Error((data && data.detail) || res.statusText || 'Erro');
      err.status = res.status;
      err.data = data;
      throw err;
    }
    return data;
  }

  window.AN_API = {
    // auth
    me:                () => req('/api/auth/me'),
    captcha:           () => req('/api/auth/captcha'),
    oauthAvailability: () => req('/api/auth/oauth-availability'),
    register:          (body) => req('/api/auth/register',    { method: 'POST', body }),
    login:             (body) => req('/api/auth/login',       { method: 'POST', body }),
    adminLogin:        (body) => req('/api/auth/admin/login', { method: 'POST', body }),
    logout:            ()     => req('/api/auth/logout',      { method: 'POST' }),
    oauthStartUrl:     (provider) => '/api/auth/oauth/' + provider,

    // products
    listProducts:      () => req('/api/products'),

    // orders
    listMyOrders:      () => req('/api/orders'),
    createOrder:       (formData) => req('/api/orders', { method: 'POST', body: formData }),

    // admin
    adminListProducts: () => req('/api/admin/products'),
    adminUpdateProduct:(id, patch) => req('/api/admin/products/' + id, { method: 'PATCH', body: patch }),
    adminSetOrderStatus:(id, status) => req('/api/admin/orders/' + id, { method: 'PATCH', body: { status } })
  };
})();
