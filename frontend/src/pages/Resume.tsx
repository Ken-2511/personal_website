// filename: Resume.tsx

import React from "react";
import { useState } from "react";
import "./Resume.css";
import { pdfjs, Document, Page } from "react-pdf";
import "react-pdf/dist/esm/Page/AnnotationLayer.css";
import "react-pdf/dist/esm/Page/TextLayer.css";
import type { PDFDocumentProxy } from "pdfjs-dist";

pdfjs.GlobalWorkerOptions.workerSrc = new URL(
    'pdfjs-dist/build/pdf.worker.min.mjs',
    import.meta.url,
  ).toString();  

const Resume: React.FC = () => {

    const pdfFile = "/resume.pdf";

    // 动态计算宽度
    const calculateWidth = (): number => {
        const maxWidth = 800;
        const availableWidth = document.documentElement.clientWidth - 32; // 2em 转换为像素（假设 1em = 16px）
        console.log("availableWidth: ", availableWidth);
        return Math.min(maxWidth, availableWidth);
    };

    const [pageWidth, setPageWidth] = useState<number>(calculateWidth());

    // 添加 resize 监听器
    React.useEffect(() => {
        const handleResize = () => setPageWidth(calculateWidth());
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, []);

    const [numPages, setNumPages] = useState<number>();

    function onDocumentLoadSuccess({ numPages: nextNumPages }: PDFDocumentProxy): void {
        setNumPages(nextNumPages);
    }

    return (
        <div className={"resume-page"}>
            <div className="resume-container">
                <Document file={pdfFile} onLoadSuccess={onDocumentLoadSuccess}>
                    <a href={pdfFile} className="download-pdf" target="_blank" rel="noopener noreferrer">
                        <img className="download-pdf-img" src="/assets/icon/pop-out.png" alt="pop-out" />
                    </a>
                    {Array.from(new Array(numPages), (_el, index) => (
                        <div className="page-container" key={`container_${index + 1}`}>
                            <Page
                                className={"resume-page"}
                                key={`page_${index + 1}`}
                                pageNumber={index + 1}
                                width={pageWidth}
                            />
                        </div>
                    ))}
                </Document>
            </div>
        </div>
    );
    
}

export default Resume;
