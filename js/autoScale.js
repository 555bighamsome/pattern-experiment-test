/**
 * 自动缩放脚本 - 让固定尺寸的界面在任何窗口大小下完整显示
 * 界面固定尺寸：1200px × 750px
 */

(function() {
    const FIXED_WIDTH = 1200;
    const FIXED_HEIGHT = 750;
    const PADDING = 20; // 留一些边距

    function calculateAndApplyScale() {
        const experimentContent = document.getElementById('experimentContent');
        if (!experimentContent) return;

        // 获取窗口可用尺寸
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;

        // 计算需要的缩放比例（留出padding空间）
        const scaleX = (windowWidth - PADDING * 2) / FIXED_WIDTH;
        const scaleY = (windowHeight - PADDING * 2) / FIXED_HEIGHT;
        
        // 取较小的缩放比例，确保完整显示
        let scale = Math.min(scaleX, scaleY);
        
        // 限制最小和最大缩放比例
        scale = Math.max(0.3, Math.min(1, scale)); // 最小30%，最大100%

        // 应用缩放
        experimentContent.style.transform = `scale(${scale})`;
        
        // 调试信息
        console.log(`Window: ${windowWidth}×${windowHeight}, Scale: ${scale.toFixed(3)}`);
    }

    // 页面加载时计算
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', calculateAndApplyScale);
    } else {
        calculateAndApplyScale();
    }

    // 窗口大小改变时重新计算
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(calculateAndApplyScale, 100);
    });

    // 提供全局函数供其他脚本调用
    window.recalculateScale = calculateAndApplyScale;
})();
