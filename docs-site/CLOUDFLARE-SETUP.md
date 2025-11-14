# Cloudflare Setup for Taminator Documentation

## Step-by-Step: Adding taminator.dev to Cloudflare

### 1. Add Site to Cloudflare

1. Log in to [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Click **"Add a Site"** (or "+ Add Site" button)
3. Enter your domain: `taminator.dev`
4. Click **"Add Site"**

### 2. Select Plan

- Choose **Free** plan (sufficient for documentation site)
- Click **"Continue"**

### 3. Review DNS Records

Cloudflare will scan your existing DNS records (if any).

**For GitLab Pages deployment:**

Add these DNS records:

| Type | Name | Content | Proxy Status | TTL |
|------|------|---------|--------------|-----|
| A | @ | 35.185.44.232 | Proxied (orange cloud) | Auto |
| CNAME | www | taminator.dev | Proxied (orange cloud) | Auto |
| TXT | _gitlab-pages-verification-code | your-verification-code | DNS only (grey cloud) | Auto |

**GitLab Pages IPs (if needed):**
- `35.185.44.232`
- `35.244.142.54`
- `35.202.148.191`
- `35.222.29.236`

Click **"Continue"**

### 4. Change Nameservers

Cloudflare will provide nameservers like:
```
bob.ns.cloudflare.com
sue.ns.cloudflare.com
```

**Update nameservers at your domain registrar:**

=== "Namecheap"
    1. Log in to Namecheap
    2. Go to Domain List → Manage
    3. Find "NAMESERVERS" section
    4. Select "Custom DNS"
    5. Enter Cloudflare nameservers
    6. Save

=== "GoDaddy"
    1. Log in to GoDaddy
    2. Go to My Products → Domains
    3. Click DNS next to your domain
    4. Click "Change" next to Nameservers
    5. Select "Custom"
    6. Enter Cloudflare nameservers
    7. Save

=== "Google Domains"
    1. Log in to Google Domains
    2. Select your domain
    3. Click "DNS" in left sidebar
    4. Scroll to "Name servers"
    5. Select "Use custom name servers"
    6. Enter Cloudflare nameservers
    7. Save

**Propagation Time:** 2-48 hours (usually < 1 hour)

### 5. Configure SSL/TLS

After nameservers are active:

1. Go to **SSL/TLS** tab
2. Set SSL/TLS encryption mode: **Full (strict)**
3. Enable these features:
   - ✅ Always Use HTTPS
   - ✅ Automatic HTTPS Rewrites
   - ✅ Minimum TLS Version: 1.2

### 6. Configure GitLab Pages

In your GitLab project (`jbyrd/taminator`):

1. Go to **Settings → Pages**
2. Click **"New Domain"**
3. Enter: `taminator.dev`
4. Copy the verification TXT record
5. Add it to Cloudflare DNS (see step 3)
6. Click **"Create New Domain"**
7. Repeat for `www.taminator.dev`

### 7. Configure Page Rules (Optional but Recommended)

Go to **Rules → Page Rules** in Cloudflare:

**Rule 1: Redirect www to apex**
- URL: `www.taminator.dev/*`
- Setting: Forwarding URL (301 Permanent Redirect)
- Destination: `https://taminator.dev/$1`

**Rule 2: Force HTTPS**
- URL: `http://taminator.dev/*`
- Setting: Always Use HTTPS

### 8. Performance Optimization

**Caching:**
- Go to **Caching → Configuration**
- Set Caching Level: **Standard**
- Browser Cache TTL: **Respect Existing Headers**

**Auto Minify:**
- Go to **Speed → Optimization**
- Enable:
  - ✅ JavaScript
  - ✅ CSS
  - ✅ HTML

**Brotli Compression:**
- Go to **Speed → Optimization**
- Enable: ✅ Brotli

### 9. Update mkdocs.yml

```yaml
site_url: https://taminator.dev
```

### 10. Deploy

```bash
cd /home/jbyrd/TAMINATOR
mkdocs build
mkdocs gh-deploy  # Or GitLab Pages deploy
```

---

## Verification Checklist

After setup complete:

- [ ] Domain resolves to GitLab Pages
- [ ] SSL certificate active (green padlock)
- [ ] `http://` redirects to `https://`
- [ ] `www.taminator.dev` redirects to `taminator.dev`
- [ ] Documentation site loads correctly
- [ ] All navigation links work

---

## Troubleshooting

### "ERR_TOO_MANY_REDIRECTS"
- **Cause:** SSL/TLS mode mismatch
- **Fix:** Set to **Full (strict)** in Cloudflare SSL/TLS settings

### "521 Web Server Is Down"
- **Cause:** GitLab Pages not configured correctly
- **Fix:** Verify DNS records and GitLab Pages domain settings

### "525 SSL Handshake Failed"
- **Cause:** GitLab Pages certificate not ready
- **Fix:** Wait 10-15 minutes for certificate provisioning

### Domain Not Resolving
- **Cause:** Nameserver propagation not complete
- **Fix:** Wait up to 48 hours, check with `dig taminator.dev NS`

---

## Quick Reference Commands

```bash
# Check nameservers
dig taminator.dev NS

# Check DNS A record
dig taminator.dev A

# Check SSL certificate
curl -vI https://taminator.dev

# Test HTTPS redirect
curl -I http://taminator.dev
```

---

## Alternative: GitHub Pages Setup

If using GitHub Pages instead of GitLab Pages:

**DNS Records:**
| Type | Name | Content | Proxy Status |
|------|------|---------|--------------|
| A | @ | 185.199.108.153 | Proxied |
| A | @ | 185.199.109.153 | Proxied |
| A | @ | 185.199.110.153 | Proxied |
| A | @ | 185.199.111.153 | Proxied |
| CNAME | www | USERNAME.github.io | Proxied |

**GitHub Pages Settings:**
1. Go to repository Settings → Pages
2. Enter custom domain: `taminator.dev`
3. Enable "Enforce HTTPS"
4. Verify DNS check passes

---

**Next Steps:** Once domain is active, deploy the documentation site!

```bash
cd /home/jbyrd/TAMINATOR
mkdocs build
# Push to GitLab/GitHub Pages
```




