// import React from "react";

// type ImageSEOProps = {
//   src: string;
//   alt: string;
//   className:string;
//   title?: string;
//   description?: string;
//   caption?: string;
//   keywords?: string[];
//   author?: string;
//   openGraph?: boolean; // Enable Open Graph tags
//   twitterCard?: boolean; // Enable Twitter Card tags
// };

// const ImageSEO: React.FC<ImageSEOProps> = ({
//   src,
//   alt,
//   className,
//   title,
//   description,
//   caption,
//   keywords = [],
//   author = "Your Brand Name",
//   openGraph = true,
//   twitterCard = true,
// }) => {
//   const metaTitle = title || alt;
//   const metaDescription = description || alt;

//   return (
//     <div style={{ padding: "20px" }}>
//       <Helmet>
//         <title>{metaTitle}</title>
//         <meta name="description" content={metaDescription} />
//         {keywords.length > 0 && (
//           <meta name="keywords" content={keywords.join(", ")} />
//         )}

//         {/* Open Graph Tags */}
//         {openGraph && (
//           <>
//             <meta property="og:title" content={metaTitle} />
//             <meta property="og:description" content={metaDescription} />
//             <meta property="og:image" content={src} />
//             <meta property="og:type" content="image" />
//           </>
//         )}

//         {/* Twitter Card Tags */}
//         {twitterCard && (
//           <>
//             <meta name="twitter:card" content="summary_large_image" />
//             <meta name="twitter:title" content={metaTitle} />
//             <meta name="twitter:description" content={metaDescription} />
//             <meta name="twitter:image" content={src} />
//           </>
//         )}

//         {/* JSON-LD Structured Data */}
//         <script type="application/ld+json">
//           {JSON.stringify({
//             "@context": "https://schema.org",
//             "@type": "ImageObject",
//             "contentUrl": src,
//             "name": metaTitle,
//             "description": metaDescription,
//             "author": {
//               "@type": "Organization",
//               "name": author,
//             },
//           })}
//         </script>
//       </Helmet>

//       <figure>
//         <img
//           src={src}
//           alt={alt}
//           className={className}
//           loading="lazy"
//         />
//         {caption && (
//           <figcaption style={{ marginTop: "8px", fontSize: "14px", color: "#555" }}>
//             {caption}
//           </figcaption>
//         )}
//       </figure>
//     </div>
//   );
// };

// export default ImageSEO;
