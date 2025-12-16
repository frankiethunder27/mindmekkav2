# Deploying to Vercel

This guide will help you deploy the MindMekka site to Vercel.

## Prerequisites

1. A Vercel account (sign up at [vercel.com](https://vercel.com))
2. Vercel CLI installed (optional, for command line deployment)
3. An email service API key (Resend or SendGrid recommended)

## Quick Deploy

### Option 1: Deploy via Vercel Dashboard (Easiest)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Import project in Vercel**
   - Go to [vercel.com/new](https://vercel.com/new)
   - Import your GitHub repository
   - Vercel will auto-detect the settings

3. **Configure Environment Variables**
   In your Vercel project settings, add these environment variables:
   - `CONTACT_EMAIL` - Your email address to receive form submissions (e.g., `hello@mindmekka.com`)
   - `FROM_EMAIL` - Email address to send from (e.g., `noreply@mindmekka.com`)
   - `RESEND_API_KEY` - Your Resend API key (recommended) OR
   - `SENDGRID_API_KEY` - Your SendGrid API key (alternative)

4. **Set up custom domain**
   - In Vercel project settings → Domains
   - Add `mindmekka.com` and `www.mindmekka.com`
   - Follow DNS configuration instructions

5. **Deploy!**
   - Click "Deploy" and wait for the build to complete

### Option 2: Deploy via Vercel CLI

1. **Install Vercel CLI**
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**
   ```bash
   vercel login
   ```

3. **Deploy**
   ```bash
   vercel
   ```
   Follow the prompts to link your project.

4. **Set environment variables**
   ```bash
   vercel env add CONTACT_EMAIL
   vercel env add FROM_EMAIL
   vercel env add RESEND_API_KEY
   ```

5. **Deploy to production**
   ```bash
   vercel --prod
   ```

## Setting Up Email Service

### Using Resend (Recommended)

1. Sign up at [resend.com](https://resend.com)
2. Create an API key
3. Verify your domain (mindmekka.com)
4. Add `RESEND_API_KEY` to Vercel environment variables

### Using SendGrid (Alternative)

1. Sign up at [sendgrid.com](https://sendgrid.com)
2. Create an API key
3. Add `SENDGRID_API_KEY` to Vercel environment variables

### Development Mode

If you don't set up an email service, the contact form will log to the console in development mode. For production, you must configure one of the email services above.

## Post-Deployment Checklist

- [ ] Test the contact form
- [ ] Verify all pages load correctly
- [ ] Check that images display properly
- [ ] Test navigation links
- [ ] Verify mobile responsiveness
- [ ] Set up custom domain (mindmekka.com)
- [ ] Configure SSL/HTTPS (automatic with Vercel)

## Troubleshooting

### Contact form not working?
- Check that environment variables are set in Vercel
- Verify your email service API key is correct
- Check Vercel function logs for errors

### Images not loading?
- Ensure all image paths are relative (they should be)
- Check that image files are committed to git

### Domain not working?
- Verify DNS settings match Vercel's requirements
- Wait for DNS propagation (can take up to 48 hours)

## File Structure

```
/
├── api/
│   └── contact.js          # Serverless function for contact form
├── css/                    # Stylesheets
├── img/                    # Images
├── js/                     # JavaScript files
├── includes/               # PHP files (not used on Vercel)
├── vercel.json             # Vercel configuration
├── package.json            # Node.js dependencies
└── [all HTML files]        # Your site pages
```

## Notes

- The PHP contact form (`includes/contact_form.php`) is replaced by the Vercel serverless function (`api/contact.js`)
- All static files (HTML, CSS, JS, images) are served directly by Vercel
- The contact form now uses `/api/contact` endpoint instead of PHP

