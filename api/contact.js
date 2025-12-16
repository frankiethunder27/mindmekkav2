// Vercel serverless function to handle contact form submissions
export default async function handler(req, res) {
  // Only allow POST requests
  if (req.method !== 'POST') {
    return res.status(405).json({ message: 'Method not allowed' });
  }

  // Get form data from request body
  const { name, email, website, inquiry, message } = req.body;

  // Validate required fields
  if (!name || !email || !message) {
    return res.status(400).json({ message: 'Missing required fields' });
  }

  // Get email recipient from environment variable
  const recipientEmail = process.env.CONTACT_EMAIL || 'hello@mindmekka.com';
  const fromEmail = process.env.FROM_EMAIL || 'noreply@mindmekka.com';

  // Prepare email content
  const emailSubject = `Contact Form: ${inquiry || 'General Inquiry'} - MindMekka`;
  const emailBody = `New Contact Form Submission:

Name: ${name}
Email: ${email}
Website: ${website || 'Not provided'}
Inquiry Type: ${inquiry || 'General Inquiry'}

Message:
${message}

---
Sent from MindMekka contact form`;

  // Send email using a service (you can use SendGrid, Resend, or similar)
  // For now, we'll use a simple approach with nodemailer or a service like Resend
  
  try {
    // Option 1: Using Resend (recommended for Vercel)
    // You'll need to install: npm install resend
    // And set RESEND_API_KEY in Vercel environment variables
    
    if (process.env.RESEND_API_KEY) {
      try {
        const { Resend } = await import('resend');
        const resend = new Resend(process.env.RESEND_API_KEY);
        
        const { data, error } = await resend.emails.send({
          from: fromEmail,
          to: recipientEmail,
          replyTo: email,
          subject: emailSubject,
          text: emailBody,
        });

        if (error) {
          console.error('Resend error:', error);
          return res.status(500).json({ message: 'Failed to send email' });
        }

        return res.status(200).json({ success: true });
      } catch (importError) {
        console.error('Failed to import Resend:', importError);
        // Fall through to other options
      }
    }

    // Option 2: Using SendGrid
    if (process.env.SENDGRID_API_KEY) {
      try {
        const sgMail = (await import('@sendgrid/mail')).default;
        sgMail.setApiKey(process.env.SENDGRID_API_KEY);
        
        const msg = {
          to: recipientEmail,
          from: fromEmail,
          replyTo: email,
          subject: emailSubject,
          text: emailBody,
        };

        await sgMail.send(msg);
        return res.status(200).json({ success: true });
      } catch (importError) {
        console.error('Failed to import SendGrid:', importError);
        // Fall through to other options
      }
    }

    // Fallback: Log to console (for development)
    console.log('Email would be sent:', {
      to: recipientEmail,
      from: fromEmail,
      subject: emailSubject,
      body: emailBody,
    });

    // In development, return success even without email service
    if (process.env.NODE_ENV === 'development' || process.env.VERCEL_ENV === 'development') {
      return res.status(200).json({ success: true });
    }

    // In production without email service configured, return error
    return res.status(500).json({ 
      message: 'Email service not configured. Please set RESEND_API_KEY or SENDGRID_API_KEY environment variable.' 
    });

  } catch (error) {
    console.error('Error sending email:', error);
    return res.status(500).json({ message: 'Failed to send email', error: error.message });
  }
}

