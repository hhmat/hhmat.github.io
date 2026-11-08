import { test, expect, type Page } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';
import { mkdirSync } from 'node:fs';

const routes = [
  ['home', '/'],
  ['about', '/about/'],
  ['projects', '/projects/'],
  ['project-recovery', '/projects/critical-element-recovery/'],
  ['project-co2', '/projects/electrochemical-co2-plasmas/'],
  ['project-hydrogen', '/projects/fuel-cells-electrolysers-hydrogen/'],
  ['project-diamond', '/projects/electron-transparent-diamond/'],
  ['project-2d-materials', '/projects/2d-materials-semiconductors/'],
  ['project-functional-materials', '/projects/functional-materials-synthesis/'],
  ['project-sodium', '/projects/sodium-battery-scale-up/'],
  ['project-chemistry', '/projects/high-throughput-chemistry/'],
  ['project-python', '/projects/research-budget-python-tool/'],
  ['project-outreach', '/projects/materials-science-public-engagement/'],
  ['publications', '/publications/'],
  ['news', '/news/'],
  ['article-co2', '/news/electrochemical-co2-plasmas-publication/'],
  ['article-chicago', '/news/ecs-chicago-co2-plasmas/'],
  ['article-axa', '/news/axa-research-fellowship-nottingham/'],
  ['article-vancouver', '/news/invited-ecs-vancouver-electrodeposition/'],
  ['article-diamond', '/news/royal-society-diamond-outreach/'],
  ['gallery', '/gallery/'],
  ['contact', '/contact/'],
] as const;
const mainRoutes = routes.filter(([name]) => !name.startsWith('project-') && !name.startsWith('article-'));

async function open(page: Page, route: string) {
  await page.goto(route, { waitUntil: 'networkidle' });
  await expect(page.locator('main')).toBeVisible();
}

test('every route renders without console errors or failed assets', async ({ page }) => {
  mkdirSync('.verification/pages', { recursive: true });
  const errors: string[] = [];
  const failures: string[] = [];
  page.on('console', (message) => { if (message.type() === 'error') errors.push(message.text()); });
  page.on('pageerror', (error) => errors.push(error.message));
  page.on('response', (response) => { if (response.status() >= 400) failures.push(`${response.status()} ${response.url()}`); });
  for (const [name, route] of routes) {
    await open(page, route);
    await expect(page.locator('h1').first()).toBeVisible();
    await page.screenshot({ path: `.verification/pages/${name}.png`, fullPage: true });
  }
  const response = await page.goto('/404.html', { waitUntil: 'networkidle' });
  expect([200, 404]).toContain(response?.status());
  await expect(page.getByRole('heading', { name: 'This page is outside the portfolio.' })).toBeVisible();
  await page.screenshot({ path: '.verification/pages/404.png', fullPage: true });
  expect(errors).toEqual([]);
  expect(failures).toEqual([]);
});

test('main pages meet WCAG 2.1 automated accessibility checks', async ({ page }) => {
  for (const [, route] of mainRoutes) {
    await open(page, route);
    const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
    expect(results.violations, `Accessibility violations on ${route}`).toEqual([]);
  }
  await open(page, '/');
  await page.locator('#theme-toggle').click();
  const darkResults = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
  expect(darkResults.violations, 'Accessibility violations in dark mode').toEqual([]);
});

test('desktop navigation and main CTA reach their destinations', async ({ page }) => {
  const navigation = [
    ['Home', '/'], ['About', '/about/'], ['Projects', '/projects/'], ['Publications', '/publications/'],
    ['News', '/news/'], ['Gallery', '/gallery/'], ['Contact', '/contact/'],
  ];
  for (const [name, destination] of navigation) {
    await open(page, '/');
    await page.locator('#primary-navigation').getByRole('link', { name, exact: true }).click();
    await expect(page).toHaveURL(`http://127.0.0.1:7100${destination}`);
  }
  await open(page, '/');
  await page.getByRole('link', { name: 'Explore selected work' }).click();
  await expect(page).toHaveURL(/\/projects\/$/);
});

test('mobile navigation opens, closes, and navigates', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 812 });
  await open(page, '/');
  await page.locator('#nav-toggle').click();
  await expect(page.locator('#nav-toggle')).toHaveAttribute('aria-expanded', 'true');
  await page.locator('#primary-navigation').getByRole('link', { name: 'About', exact: true }).click();
  await expect(page).toHaveURL(/\/about\/$/);
  await expect(page.locator('#nav-toggle')).toHaveAttribute('aria-expanded', 'false');
});

test('theme selection persists after reload', async ({ page }) => {
  await open(page, '/');
  const initial = await page.locator('html').getAttribute('data-theme');
  await page.locator('#theme-toggle').click();
  const changed = initial === 'dark' ? 'light' : 'dark';
  await expect(page.locator('html')).toHaveAttribute('data-theme', changed);
  await page.reload({ waitUntil: 'networkidle' });
  await expect(page.locator('html')).toHaveAttribute('data-theme', changed);
});

test('site search finds and opens a project', async ({ page }) => {
  await open(page, '/');
  await page.keyboard.press('Control+k');
  await expect(page.locator('#site-search')).toBeVisible();
  await page.locator('#site-search-input').fill('critical element');
  await expect(page.locator('#search-status')).toContainText('result');
  await page.locator('.search-result-title', { hasText: 'Critical & Rare Earth Element Recovery' }).click();
  await expect(page).toHaveURL(/\/projects\/critical-element-recovery\/$/);
});

test('hydrogen project links to both related publications', async ({ page }) => {
  await open(page, '/projects/fuel-cells-electrolysers-hydrogen/');
  const links = page.locator('.article-body a[href^="https://doi.org/"]');
  await expect(links).toHaveCount(2);
  await expect(links.nth(0)).toHaveAttribute('href', 'https://doi.org/10.1002/smll.202205885');
  await expect(links.nth(1)).toHaveAttribute('href', 'https://doi.org/10.1021/acscatal.7b02701');
});

test('project and publication filters and citation copying work', async ({ page, context }) => {
  await context.grantPermissions(['clipboard-read', 'clipboard-write']);
  await open(page, '/projects/');
  await page.getByRole('button', { name: 'Data Science', exact: true }).click();
  await expect(page.locator('[data-filter-item]:visible')).toHaveCount(1);
  await expect(page.locator('[data-result-count]')).toHaveText('1 item shown');
  await page.getByRole('searchbox', { name: 'Search projects' }).fill('not-a-real-project');
  await expect(page.locator('[data-filter-empty]')).toBeVisible();

  await open(page, '/publications/');
  await page.getByRole('button', { name: 'Thesis', exact: true }).click();
  await expect(page.locator('[data-filter-item]:visible')).toHaveCount(1);
  await page.getByRole('button', { name: 'Copy citation' }).click();
  await expect(page.locator('.copy-status:visible')).toHaveText('Citation copied.');
});

test('gallery lightbox opens and closes with Escape', async ({ page }) => {
  await open(page, '/gallery/');
  await page.getByRole('button', { name: 'Enlarge Plasma electrochemistry image' }).click();
  await expect(page.locator('#gallery-lightbox')).toBeVisible();
  await expect(page.locator('#lightbox-title')).toHaveText('Plasma electrochemistry');
  await page.keyboard.press('Escape');
  await expect(page.locator('#gallery-lightbox')).not.toBeVisible();
});

test('contact form hides email addresses and sends validated enquiries', async ({ page }) => {
  await open(page, '/contact/');
  await expect(page.locator('a[href^="mailto:"]')).toHaveCount(0);
  await expect(page.locator('body')).not.toContainText(/haytham\.husseinem@gmail\.com|hemaihussein@gmail\.com/i);
  await page.getByRole('button', { name: 'Send message' }).click();
  await expect(page.locator('#name-error')).not.toBeEmpty();

  let submittedUrl = '';
  let submittedBody = '';
  await page.route('https://formsubmit.co/ajax/*', async (route) => {
    submittedUrl = route.request().url();
    submittedBody = route.request().postData() || '';
    await route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ success: 'true' }) });
  });
  await page.locator('#contact-name').fill('Test Visitor');
  await page.locator('#contact-email-input').fill('visitor@example.com');
  await page.locator('#contact-subject').fill('Research enquiry');
  await page.locator('#contact-message').fill('I would like to discuss a potential research collaboration.');
  await page.getByRole('button', { name: 'Send message' }).click();
  await expect(page.locator('#form-status')).toHaveAttribute('data-state', 'success');
  await expect(page.locator('#form-status-text')).toContainText('submitted successfully');
  expect(submittedUrl).toBe('https://formsubmit.co/ajax/hemaihussein@gmail.com');
  expect(submittedBody).toContain('Website enquiry: Research enquiry');
  expect(submittedBody).toContain('I would like to discuss a potential research collaboration.');
  await expect(page.locator('#contact-name')).toHaveValue('');

  await page.unroute('https://formsubmit.co/ajax/*');
  await page.route('https://formsubmit.co/ajax/*', async (route) => {
    await route.fulfill({ status: 503, contentType: 'application/json', body: JSON.stringify({ success: 'false' }) });
  });
  await page.locator('#contact-name').fill('Test Visitor');
  await page.locator('#contact-email-input').fill('visitor@example.com');
  await page.locator('#contact-subject').fill('Research enquiry');
  await page.locator('#contact-message').fill('I would like to discuss a potential research collaboration.');
  await page.getByRole('button', { name: 'Send message' }).click();
  await expect(page.locator('#form-status')).toHaveAttribute('data-state', 'error');
  await expect(page.locator('#form-status-text')).toContainText('could not be sent');
});

test('CV page, PDF, and website links are unavailable', async ({ page }) => {
  await open(page, '/');
  await expect(page.getByRole('link', { name: /CV|Curriculum vitae/i })).toHaveCount(0);
  const pageResponse = await page.request.get('/cv/');
  expect(pageResponse.status()).toBe(404);
  const pdfResponse = await page.request.get('/cv/haytham-hussein-cv.pdf');
  expect(pdfResponse.status()).toBe(404);
});

test('responsive layouts do not overflow at required breakpoints', async ({ page }) => {
  mkdirSync('.verification/mobile', { recursive: true });
  mkdirSync('docs/mockups', { recursive: true });
  for (const width of [375, 768, 1024, 1440]) {
    await page.setViewportSize({ width, height: 900 });
    for (const [, route] of mainRoutes) {
      await open(page, route);
      const dimensions = await page.evaluate(() => ({ scroll: document.documentElement.scrollWidth, viewport: window.innerWidth }));
      expect(dimensions.scroll, `${route} overflows at ${width}px`).toBeLessThanOrEqual(dimensions.viewport + 1);
    }
  }
  for (const [name, route] of mainRoutes) {
    await page.setViewportSize({ width: 375, height: 812 });
    await open(page, route);
    await page.screenshot({ path: `.verification/mobile/${name}.png`, fullPage: true });
  }
  await page.setViewportSize({ width: 1440, height: 1000 });
  await open(page, '/');
  await page.screenshot({ path: 'docs/mockups/home-desktop.png', fullPage: true });
  await page.setViewportSize({ width: 375, height: 812 });
  await open(page, '/');
  await page.screenshot({ path: 'docs/mockups/home-mobile.png', fullPage: true });
});

test('home page stays within the static performance budget', async ({ page }) => {
  await open(page, '/');
  const metrics = await page.evaluate(() => {
    const resources = performance.getEntriesByType('resource') as PerformanceResourceTiming[];
    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    return {
      requests: resources.length + 1,
      bytes: resources.reduce((total, entry) => total + entry.encodedBodySize, 0) + navigation.encodedBodySize,
    };
  });
  console.log(`Home page: ${metrics.requests} requests, ${Math.round(metrics.bytes / 1024)} KiB transferred`);
  expect(metrics.requests).toBeLessThan(45);
  expect(metrics.bytes).toBeLessThan(1_500_000);
});
