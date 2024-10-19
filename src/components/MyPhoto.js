import React, { useState, useEffect } from "react";
import "./MyPhoto.css";

function MyPhoto() {
    // 图片数组
    const images = [
        process.env.PUBLIC_URL + "/assets/photo1.png",
        process.env.PUBLIC_URL + "/assets/photo2.png",
    ];

    // 使用 useState 钩子来保存当前显示的图片索引和动画状态
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const [isFading, setIsFading] = useState(false);

    useEffect(() => {
        const interval = setInterval(() => {
            // 先设置淡出状态
            setIsFading(true);

            // 在动画结束后切换图片，保持与 CSS 动画时间一致
            setTimeout(() => {
                setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
                setIsFading(false);
            }, 1000);
        }, 5000);

        // 清理定时器
        return () => clearInterval(interval);
    }, [images.length]);

    return (
        <div className="my-photo">
            <img
                src={images[currentImageIndex]}
                alt="Yongkang"
                className={`photo ${isFading ? 'fade' : 'fade-in'}`}
            />
        </div>
    );
}

export default MyPhoto;
