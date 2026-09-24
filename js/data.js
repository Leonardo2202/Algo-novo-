window.AN_DATA = {
  defaultPhone: '+351 939 017 483',
  defaultLang: 'pt',
  langCodes: ['pt', 'en', 'fr', 'de'],
  langLabels: { pt: 'PT', en: 'EN', fr: 'FR', de: 'DEU' },
  langNames:  { pt: 'Português', en: 'English', fr: 'Français', de: 'Deutsch' },
  langFlags:  { pt: '🇵🇹', en: '🇬🇧', fr: '🇫🇷', de: '🇩🇪' },

  categoryOrder: ['all', 'tshirts', 'hoodies', 'embroidery', 'accessories'],
  sizes: ['XS', 'S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXXL'],
  artEmail: 'pedidos@algonovo.pt',
  maxArtBytes: 8 * 1024 * 1024,

  products: [
    { id: 'p1', catKey: 'tshirts',     price: 24.9, img: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800&h=1000&fit=crop' },
    { id: 'p2', catKey: 'tshirts',     price: 29.9, img: 'https://images.unsplash.com/photo-1503341504253-dff4815485f1?w=800&h=1000&fit=crop' },
    { id: 'p3', catKey: 'hoodies',     price: 54.9, img: 'https://images.unsplash.com/photo-1556821840-3a63f95609a7?w=800&h=1000&fit=crop' },
    { id: 'p4', catKey: 'hoodies',     price: 46.9, img: 'https://images.unsplash.com/photo-1578681994506-b8f463449011?w=800&h=1000&fit=crop' },
    { id: 'p5', catKey: 'embroidery',  price: 39.9, img: 'https://images.unsplash.com/photo-1586790170083-2f9ceadc732d?w=800&h=1000&fit=crop' },
    { id: 'p6', catKey: 'accessories', price: 22.9, img: 'https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=800&h=1000&fit=crop' },
    { id: 'p7', catKey: 'accessories', price: 16.9, img: 'https://images.unsplash.com/photo-1597481499750-3e6b22637e12?w=800&h=1000&fit=crop' },
    { id: 'p8', catKey: 'hoodies',     price: 62.9, img: 'https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=800&h=1000&fit=crop' }
  ],

  filterBaseStyle: {
    borderRadius: '999px', padding: '11px 22px', cursor: 'pointer',
    fontSize: '11px', letterSpacing: '.2em', textTransform: 'uppercase',
    transition: 'all .35s ease'
  },
  filterActiveStyle: {
    background: 'linear-gradient(135deg, #631C99 0%, #852753 55%, #C54A2D 100%)',
    color: '#F0EEEB', border: '1px solid transparent',
    boxShadow: '0 10px 24px rgba(99,28,153,.22)'
  },
  filterIdleStyle: {
    background: 'transparent', color: '#5a4f61',
    border: '1px solid rgba(99,28,153,.20)'
  },
  langOptionBase: {
    display: 'flex', alignItems: 'center', gap: '12px', width: '100%',
    background: 'transparent', border: 'none', cursor: 'pointer',
    padding: '10px 14px', borderRadius: '8px',
    fontSize: '13px', color: '#1b1620', textAlign: 'left',
    transition: 'background .2s ease'
  },
  langOptionActive: {
    background: 'rgba(99,28,153,.08)', color: '#631C99'
  }
};
