# Deployment Guide for mindmekka.com

This static website with PHP contact form needs to be deployed to a web server that supports PHP.

## Deployment Options

### Option 1: Traditional Web Hosting (FTP/SFTP)

If you have traditional web hosting (cPanel, shared hosting, VPS, etc.):

1. **Upload all files** to your web server's public directory (usually `public_html`, `www`, or `htdocs`)
2. **Ensure PHP is enabled** on your server
3. **Update contact form email** in `includes/contact_form.php` (line 14) with your actual email address
4. **Set proper file permissions** (typically 644 for files, 755 for directories)

**FTP/SFTP Tools:**
- FileZilla (GUI)
- Cyberduck (GUI)
- `scp` or `rsync` (command line)

**Example using rsync:**
```bash
rsync -avz --exclude '.git' --exclude 'Site Content' \
  /Users/chovy/MM\ Site\ V2/ user@mindmekka.com:/path/to/public_html/
```

### Option 2: GitHub + GitHub Actions

1. Push code to GitHub repository
2. Set up GitHub Actions workflow to deploy on push
3. Configure secrets for FTP/SFTP credentials

### Option 3: Modern Platforms (Netlify/Vercel)

These platforms require converting the PHP contact form to a serverless function or using a third-party service like Formspree.

## Pre-Deployment Checklist

- [ ] Update email address in `includes/contact_form.php`
- [ ] Test contact form functionality
- [ ] Verify all image paths are correct
- [ ] Check that all CSS and JS files load properly
- [ ] Test on mobile devices
- [ ] Verify sitemap.xml is accessible

## Important Files to Deploy

- All HTML files (in root and subdirectories)
- `css/` directory
- `js/` directory
- `img/` directory
- `includes/` directory (contains PHP contact form)
- `favicon.jpg`
- `style.css`
- `sitemap.xml`

## Files NOT to Deploy

- `Site Content/` directory (documentation/design files)
- `.git/` directory
- `.gitignore`
- `DEPLOYMENT.md`

## Post-Deployment

1. Test the contact form
2. Verify all pages load correctly
3. Check that images display properly
4. Test navigation links
5. Verify mobile responsiveness

