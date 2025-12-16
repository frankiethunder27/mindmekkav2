# MindMekka Website

Static website for MindMekka, deployed on Vercel.

## Quick Start

### Deploy to Vercel

1. **Push to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Ready for Vercel deployment"
   git push
   ```

2. **Deploy via Vercel Dashboard**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Add environment variables (see below)
   - Deploy!

3. **Set Environment Variables in Vercel**
   - `CONTACT_EMAIL` = `hello@mindmekka.com` (or your email)
   - `FROM_EMAIL` = `noreply@mindmekka.com`
   - `RESEND_API_KEY` = Your Resend API key (get one at [resend.com](https://resend.com))

4. **Connect Custom Domain**
   - In Vercel project → Settings → Domains
   - Add `mindmekka.com` and follow DNS instructions

## Local Development

```bash
# Install dependencies
npm install

# Run local dev server (requires Vercel CLI)
npm install -g vercel
vercel dev
```

## Project Structure

- `/api/contact.js` - Serverless function for contact form
- `/js/formHandler.js` - Form submission handler (updated for Vercel)
- All HTML files in root and subdirectories
- Static assets in `/css`, `/js`, `/img`

## Contact Form

The contact form uses a Vercel serverless function instead of PHP. It supports:
- Resend (recommended)
- SendGrid (alternative)
- Development mode (logs to console)

See `VERCEL_DEPLOY.md` for detailed deployment instructions.

