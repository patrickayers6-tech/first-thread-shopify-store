const { test, expect } = require('@playwright/test');

const base = 'http://127.0.0.1:8899';
const routes = [
  '/', '/shop.html', '/cart.html',
  '/products/night-garden-first-stitch-mini.html',
  '/products/lucky-sardine-first-stitch-mini.html',
  '/products/little-victory-first-stitch-mini.html',
  '/products/pick-any-two-first-stitch-minis.html',
  '/products/stitch-rescue-pack.html',
  '/pages/our-story.html', '/pages/how-it-works.html', '/pages/beginner-help.html',
  '/pages/faq.html', '/pages/founding-drop-policy.html', '/pages/shipping-returns.html', '/pages/contact.html'
];

for (const route of routes) {
  test(`route ${route} loads`, async ({ request }) => {
    const res = await request.get(base + route);
    expect(res.status()).toBe(200);
  });
}

test('home merchandising, form, and layout work', async ({ page }) => {
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(base + '/');
  await expect(page).toHaveTitle(/Beginner mini needlepoint kits/);
  await expect(page.locator('h1')).toContainText('A first project you can actually finish');
  await expect(page.locator('.fts-product-card')).toHaveCount(3);
  await expect(page.locator('text=No fake reviews. No invented finish times.')).toBeVisible();
  const sizes = await page.evaluate(() => ({scroll: document.documentElement.scrollWidth, client: document.documentElement.clientWidth}));
  expect(sizes.scroll).toBeLessThanOrEqual(sizes.client + 1);
  await page.locator('[data-preview-waitlist] input').fill('test@example.com');
  await page.locator('[data-preview-waitlist] button').click();
  await expect(page.locator('.preview-form-message')).toContainText('saved locally');
  expect(await page.evaluate(() => localStorage.getItem('ftsPreviewEmail'))).toBe('test@example.com');
  expect(errors).toEqual([]);
  await page.screenshot({path: 'tests/storefront-desktop.png', fullPage: true});
});

test('mobile navigation and responsive layout work', async ({ page }) => {
  await page.setViewportSize({width: 390, height: 844});
  await page.goto(base + '/');
  const sizes = await page.evaluate(() => ({scroll: document.documentElement.scrollWidth, client: document.documentElement.clientWidth}));
  expect(sizes.scroll).toBeLessThanOrEqual(sizes.client + 1);
  await page.locator('.preview-menu').click();
  await expect(page.locator('.preview-links')).toHaveClass(/open/);
  await expect(page.locator('.preview-links a')).toHaveCount(5);
  await page.screenshot({path: 'tests/storefront-mobile.png', fullPage: true});
});

test('product disclosure and locked checkout work', async ({ page }) => {
  await page.goto(base + '/products/night-garden-first-stitch-mini.html');
  await expect(page.locator('h1')).toContainText('Night Garden');
  await expect(page.locator('.product-gallery img')).toHaveCount(3);
  await expect(page.locator('.product-mini-note')).toContainText('Pre-launch preview');
  await page.locator('[data-locked-checkout]').click();
  await expect(page.locator('.preview-toast')).toHaveClass(/show/);
  await expect(page.locator('.preview-toast')).toContainText('Checkout is intentionally locked');
});

test('agent discovery endpoints and product feeds are valid', async ({ request }) => {
  for (const route of ['/agents.md', '/llms.txt', '/llms-full.txt', '/catalog.json', '/products.json', '/feed.json', '/openai_products.csv', '/google_merchant_products.csv', '/sitemap.xml', '/robots.txt']) {
    const res = await request.get(base + route);
    expect(res.status(), route).toBe(200);
    expect((await res.body()).length, route).toBeGreaterThan(50);
  }
  const catalog = await (await request.get(base + '/catalog.json')).json();
  expect(catalog).toHaveLength(5);
  for (const product of catalog) {
    expect(product.availability).toBe('out_of_stock');
    expect(product.checkout_enabled).toBe(false);
    expect(product.url).toMatch(/^https:\/\//);
    expect(product.image_url).toMatch(/^https:\/\//);
  }
  const agents = await (await request.get(base + '/agents.md')).text();
  expect(agents).toContain('Do not describe them as available to purchase yet');
  expect(agents).toContain('OpenAI-compatible discovery feed');
});

test('product pages expose accurate Product structured data', async ({ page }) => {
  await page.goto(base + '/products/night-garden-first-stitch-mini.html');
  const blocks = await page.locator('script[type="application/ld+json"]').allTextContents();
  const parsed = blocks.map(text => JSON.parse(text));
  const product = parsed.find(item => item['@type'] === 'Product');
  expect(product.name).toContain('Night Garden');
  expect(product.sku).toBe('FTS-NG-01');
  expect(product.offers.priceCurrency).toBe('USD');
  expect(product.offers.availability).toBe('https://schema.org/OutOfStock');
  expect(product).not.toHaveProperty('aggregateRating');
});

test('all rendered storefront images resolve', async ({ page, request }) => {
  await page.goto(base + '/');
  const srcs = await page.locator('img').evaluateAll(images => images.map(image => image.currentSrc || image.src));
  for (const src of srcs) {
    const res = await request.get(src);
    expect(res.status(), src).toBe(200);
    expect(res.headers()['content-type'], src).toMatch(/^image\//);
  }
});
