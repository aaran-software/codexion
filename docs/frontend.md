
# Frontend Project Structure

```
codexsion/
│
├── React/ # React frontend application
│
│ ├── public/ # Static files like index.html, icons, etc.
│ │ ├── assets/
│ │ │ ├── logo/ # Logo assets
│ │ │ ├── static-images/ # Other static images
│ │ ├── JSON/
│ │ │ ├── settings.json # Branding and layout configs
│ │ │ ├── app.json # App-wide dynamic configuration
│ │
│ ├── src/
│ │
│ │ ├── resource/ # Reusable design system and layout resources
│ │ │ ├── components/ # Atomic reusable UI components
│ │ │ │ ├── input/
│ │ │ │ ├── accordion/
│ │ │ │ ├── alert/
│ │ │ │ ├── tooltip/
│ │ │ │ ├── etc/
│ │ │
│ │ │ ├── UI Blocks/ # Composite UI blocks
│ │ │ │ ├── cart/
│ │ │ │ ├── header/
│ │ │ │ ├── footer/
│ │ │ │ ├── team/
│ │ │ │ ├── carousel/
│ │ │ │ ├── dynamictable/
│ │ │ │ ├── etc/
│ │ │
│ │ │ ├── Layouts/ # Page layout templates
│ │ │ │ ├── with-left-navbar/
│ │ │ │ ├── with-top-navbar/
│ │ │ │ ├── no-header-navbar/
│ │ │ │ ├── login/
│ │ │ │ ├── signup/
│ │ │ │ ├── etc/
│
│ │ ├── pages/ # All route-level pages
│ │ │
│ │ │ ├── CMS/ # CMS content pages
│ │ │ │ ├── home/
│ │ │ │ ├── about/
│ │ │ │ ├── service/
│ │ │ │ ├── contact/
│ │ │ │ ├── product/
│ │ │
│ │ │ ├── apps/ # Functional app modules
│ │ │ │
│ │ │ │ ├── ecart/ # E-commerce module
│ │ │ │ │ ├── home/ # Landing page
│ │ │ │ │ ├── category/
│ │ │ │ │ ├── product/
│ │ │ │ │ ├── cart/
│ │ │ │ │ ├── wishlist/
│ │ │ │ │ ├── login/
│ │ │ │ │ ├── signup/
│ │ │ │ │ ├── seller-auth/ # Seller login & signup
│ │ │ │ │ ├── dashboards/
│ │ │ │ │ │ ├── admin/ # Admin dashboard (individual company)
│ │ │ │ │ │ ├── seller/ # Seller dashboard (multi-vendor)
│ │ │ │ │ ├── orders/ # Order history, status, invoices
│ │ │ │ │ ├── checkout/ # Checkout flow
│ │ │ │ │ ├── payment/ # Payment gateway integration
│ │ │ │ │ ├── profile/ # User profile & settings
│ │ │ │ │ ├── reviews/ # Product reviews & ratings
│ │ │ │ │ ├── notifications/ # Alerts, order updates, etc.
│
│ │ │ │ ├── CRM/ # CRM - Customer Relationship Management
│ │ │ │ │ ├── dashboard/ # CRM overview & analytics
│ │ │ │ │ ├── contacts/ # Manage leads and contacts
│ │ │ │ │ ├── companies/ # Business clients or organizations
│ │ │ │ │ ├── deals/ # Deal pipeline (Kanban)
│ │ │ │ │ ├── activities/ # Tasks, calls, meetings
│ │ │ │ │ ├── tickets/ # Customer support tickets
│ │ │ │ │ ├── reports/ # Performance reports and analytics
│ │ │ │ │ ├── settings/ # Workflow automation, roles, permissions
│ │ │ │ │ ├── campaigns/ # Email/SMS marketing campaigns
│ │ │ │ │ ├── automation/ # Rule-based triggers and sequences
│
│ │ │ │ ├── LMS/ # LMS - Learning Management System
│ │ │ │ │ ├── dashboard/ # LMS overview and metrics
│ │ │ │ │ ├── courses/ # Course management (add/edit/view)
│ │ │ │ │ ├── lessons/ # Lesson content per course
│ │ │ │ │ ├── users/ # Student and instructor management
│ │ │ │ │ ├── enrollments/ # Enrollment status & history
│ │ │ │ │ ├── quizzes/ # Quiz and assessment module
│ │ │ │ │ ├── certificates/ # Completion certificates
│ │ │ │ │ ├── settings/ # Grading, roles, permissions
│ │ │ │ │ ├── discussion/ # Course discussions / forums
│ │ │ │ │ ├── assignments/ # Student submissions
│
│ │ │ │ ├── billing/ # Billing & accounting management
│ │ │ │ │ ├── entries/
│ │ │ │ │ │ ├── sales/
│ │ │ │ │ │ ├── purchase/
│ │ │ │ │ │ ├── receipt/
│ │ │ │ │ │ ├── payment/
│ │ │ │ │ ├── master/
│ │ │ │ │ │ ├── contact/
│ │ │ │ │ │ ├── product/
│ │ │ │ │ │ ├── company/
│ │ │ │ │ │ ├── order/
│ │ │ │ │ │ ├── styles/
│ │ │ │ │ ├── books/
│ │ │ │ │ │ ├── account-heads/
│ │ │ │ │ │ ├── ledger-group/
│ │ │ │ │ │ ├── ledger/
│ │ │ │ │ ├── transaction/
│ │ │ │ │ │ ├── account-books/
│ │ │ │ │ ├── common/
│ │ │ │ │ │ ├── city/
│ │ │ │ │ │ ├── state/
│ │ │ │ │ │ ├── payment-types/
│ │ │ │ │ │ ├── contact-type/
│ │ │ │ │ │ ├── pincode/
│ │ │ │ │ │ ├── etc/
│
│ │ ├── routes/ # Application routing and route guards
│ │ │ └── index.tsx # Combines all routes
│ │ │ └── ecartRoutes.tsx # Routes only for ecart
│ │ │ └── cmsRoutes.tsx # Routes only for CMS
│ │ │ 
│ │ ├── context/ # App-level contexts (e.g., AuthContext, ThemeContext)
│ │ ├
│ │ ├── services/
│ │ │ ├── api.ts
│ │ │ ├── auth.service.ts
│ │ │ ├── user.service.ts
│ │ │ ├── upload.service.ts
│ │ ├
│ │ ├── Global/
│ │ │ ├── types
│ │ │ ├── utils
│ │ │ ├── context
│ │ │ │ ├── AuthContext
│ │ │ │ ├── AppContext
│ │ │ ├── config
│ │ │ ├── App.tsx # App root component
│ │ │ ├── theme.css # App-wide styles
│ │ ├
│ │ └── main.tsx # React app entry point
│
│ ├── .env # Environment variable definitions
│ ├── tsconfig.json # TypeScript configuration
│ ├── vite.config.ts / webpack.config.js # Build configuration
│ ├── package.json # Project dependencies & scripts
│ └── README.md # Project overview and documentation
```