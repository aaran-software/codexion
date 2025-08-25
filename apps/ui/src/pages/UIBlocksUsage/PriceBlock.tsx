import React from 'react'
import DocsWrapper from '../DocsWrapper'
import Pricing from "../../../../../resources/UIBlocks/pricingcard/Pricing";

function PriceBlock() {
   const plans = [
    {
      id: "free",
      name: "Free",
      price: 0,
      description: "Basic features for individuals",
      features: [
        { id: 1, text: "Access to core features" },
        { id: 2, text: "1 Project" },
        { id: 3, text: "Community Support" },
        { id: 4, text: "Basic Analytics" },
        { id: 5, text: "Email Alerts" },
        { id: 6, text: "Single User" },
        { id: 7, text: "Basic Templates" },
        { id: 8, text: "Limited Storage" },
      ],
    },
    {
      id: "pro",
      name: "Pro",
      price: 15,
      description: "Advanced features for professionals",
      highlight: true, // highlight this plan
      features: [
        { id: 1, text: "Everything in Free" },
        { id: 2, text: "Unlimited Projects" },
        { id: 3, text: "Priority Support" },
        { id: 4, text: "Advanced Analytics" },
        { id: 5, text: "Team Collaboration" },
        { id: 6, text: "Export Data" },
        { id: 7, text: "Custom Branding" },
        { id: 8, text: "Cloud Backup" },
        { id: 9, text: "Role Management" },
      ],
    },
    {
      id: "premium",
      name: "Premium",
      price: 30,
      description: "All features for large teams",
      features: [
        { id: 1, text: "Everything in Pro" },
        { id: 2, text: "Dedicated Manager" },
        { id: 3, text: "Custom Integrations" },
        { id: 4, text: "API Access" },
        { id: 5, text: "Advanced Security" },
        { id: 6, text: "24/7 Support" },
        { id: 7, text: "Custom Workflows" },
        { id: 8, text: "Unlimited Storage" },
      ],
    },
  ];
  return (
    <div>
      <DocsWrapper
        title="HeaderPortfolio"
        propDocs={[]}
        paths={{
          file: "/resources/UIBlocks/header/AppFooter",
          usedIn: ["/pages/Home.tsx"],
          reusableIn: [
            "Landing sections",
            "Portfolio Previews",
            "Hero Backgrounds",
            "Scroll Animations",
          ],
        }}
      >
         <Pricing plans={plans} />
      </DocsWrapper>
    </div>
  )
}

export default PriceBlock