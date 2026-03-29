function copytext(e) {
    const text = e.innerText.trim();

    navigator.clipboard.writeText(text).then(() => {
        showAndroidToast("Copied to clipboard");
    }).catch(err => {
        showAndroidToast("Failed to copy!");
    });
}

function showAndroidToast(message) {
    // 1. إنشاء العنصر
    const toast = document.createElement("div");
    toast.innerText = message;

    // 2. ستايل أندرويد (Dark Mode Native Look)
    Object.assign(toast.style, {
        position: "fixed",
        bottom: "12%", // رفعتها شوية عشان تكون فوق الـ Navigation Bar بتاع الموبايل
        left: "50%",
        transform: "translateX(-50%)",
        backgroundColor: "#323232", // لون أندرويد الرسمي للـ Toasts
        color: "#F1F1F1",
        padding: "12px 24px",
        borderRadius: "25px",
        fontSize: "14px",
        fontFamily: "Roboto, sans-serif",
        zIndex: "10000",
        opacity: "0",
        transition: "opacity 0.3s ease-in-out",
        pointerEvents: "none",
        whiteSpace: "nowrap",
        boxShadow: "0 4px 6px rgba(0,0,0,0.2)"
    });

    // 3. الاهتزاز (مع التأكد إن المتصفح يدعمه)
    if (typeof navigator.vibrate === "function") {
        navigator.vibrate(40); // هزة سريعة جداً زي الـ System Feedback
    }

    document.body.appendChild(toast);

    // 4. تفعيل الظهور
    setTimeout(() => { toast.style.opacity = "1"; }, 10);

    // 5. الاختفاء والمسح
    setTimeout(() => {
        toast.style.opacity = "0";
        setTimeout(() => {
            if (toast.parentNode) {
                document.body.removeChild(toast);
            }
        }, 300);
    }, 2000);
}