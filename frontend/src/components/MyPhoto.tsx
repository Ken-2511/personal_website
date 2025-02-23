import { useState, useEffect, useMemo } from "react";
import "./MyPhoto.css";

function MyPhoto() {
    // 使用 useMemo 缓存图片数组，避免每次渲染时重新初始化
    const images = useMemo(() => [
        import.meta.env.VITE_PUBLIC_URL + "/assets/photo1.png",
        import.meta.env.VITE_PUBLIC_URL + "/assets/butterfly.jpg",
        import.meta.env.VITE_PUBLIC_URL + "/assets/photo2.png",
        import.meta.env.VITE_PUBLIC_URL + "/assets/photogate.jpg",
        // process.env.PUBLIC_URL + "/assets/rb.jpg",
        import.meta.env.VITE_PUBLIC_URL + "/assets/kp.jpg",
        import.meta.env.VITE_PUBLIC_URL + "/assets/toronto.jpg",
    ], []);

    // 使用 useState 钩子保存当前显示的图片索引、动画状态和加载状态
    const [currentImageIndex, setCurrentImageIndex] = useState(0);
    const [isFading, setIsFading] = useState(false);
    const [isLoaded, setIsLoaded] = useState(false);

    // 预加载图片函数
    const preloadImages = (imageArray: string[]) => {
        return imageArray.map((src) => {
            const img = new Image();
            img.src = src;
            return img;
        });
    };

    // 预加载所有图片
    useEffect(() => {
        const loadedImages = preloadImages(images);

        // 设置所有图片加载完毕的状态
        const handleImagesLoaded = () => {
            setIsLoaded(true);
        };

        // 如果所有图片都已经加载完毕，设置加载状态为 true
        if (loadedImages.every((img: HTMLImageElement) => img.complete)) {
            handleImagesLoaded();
        } else {
            // 监听图片加载完成
            loadedImages.forEach((img: HTMLImageElement) => {
                img.onload = handleImagesLoaded;
            });
        }
    }, [images]); // 使用 useMemo 的 images，不会重新生成

    useEffect(() => {
        if (!isLoaded) return; // 如果图片还未加载完成，不执行后续的逻辑

        const interval = setInterval(() => {
            setIsFading(true);

            // 在动画结束后切换图片，保持与 CSS 动画时间一致
            setTimeout(() => {
                setCurrentImageIndex((prevIndex) => (prevIndex + 1) % images.length);
                setIsFading(false);
            }, 1000); // 1秒的淡出动画时间
        }, 5000); // 每5秒切换图片

        // 清理定时器
        return () => clearInterval(interval);
    }, [images.length, isLoaded]); // 确保定时器依赖图片数组长度和加载状态

    return (
        <div className="my-photo">
            {isLoaded ? (
                <img
                    src={images[currentImageIndex]}
                    alt="Yongkang"
                    className={`photo ${isFading ? "fade" : "fade-in"}`}
                />
            ) : (
                <p>Loading...</p>
            )}
        </div>
    );
}

export default MyPhoto;
