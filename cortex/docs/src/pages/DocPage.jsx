import React, { useEffect, useState } from 'react';
import MarkdownRenderer from '../components/MarkdownRenderer';

export default function DocPage({ slug }) {
    const [content, setContent] = useState('');

    useEffect(() => {
        fetch(`/api/docs/${slug}`)
            .then(res => res.json())
            .then(data => setContent(data.content));
    }, [slug]);

    return <MarkdownRenderer content={content} />;
}