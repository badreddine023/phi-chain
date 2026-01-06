class SkeletonLoader {
    constructor() {
        this.skeletonContainer = null;
        this.minDisplayTime = 1500; // Minimum display time (ms)
        this.startTime = Date.now();
    }
    
    init() {
        this.createSkeletonScreen();
        this.simulateContentLoading();
    }
    
    createSkeletonScreen() {
        this.skeletonContainer = document.createElement('div');
        this.skeletonContainer.id = 'skeleton-container';
        
        const skeletonHTML = `
            <!-- Header -->
            <div class="skeleton-header">
                <div class="skeleton-logo skeleton-shimmer"></div>
                <div style="display: flex; gap: 2rem;">
                    <div style="width: 80px; height: 20px;" class="skeleton-shimmer"></div>
                    <div style="width: 80px; height: 20px;" class="skeleton-shimmer"></div>
                    <div style="width: 80px; height: 20px;" class="skeleton-shimmer"></div>
                </div>
            </div>
            
            <!-- Hero Section -->
            <section class="skeleton-hero">
                <div class="skeleton-hero-title skeleton-shimmer"></div>
                <div class="skeleton-hero-subtitle skeleton-shimmer"></div>
                <div>
                    <span class="skeleton-cta skeleton-shimmer"></span>
                    <span class="skeleton-cta skeleton-shimmer" style="animation-delay: 0.4s;"></span>
                </div>
            </section>
            
            <!-- Wallet Cards -->
            <div class="skeleton-grid">
                <div class="skeleton-card">
                    <div class="skeleton-card-icon skeleton-shimmer"></div>
                    <div class="skeleton-card-title skeleton-shimmer"></div>
                    <div class="skeleton-card-text skeleton-shimmer"></div>
                    <div class="skeleton-card-button skeleton-shimmer"></div>
                </div>
                <div class="skeleton-card">
                    <div class="skeleton-card-icon skeleton-shimmer" style="animation-delay: 0.1s;"></div>
                    <div class="skeleton-card-title skeleton-shimmer" style="animation-delay: 0.1s;"></div>
                    <div class="skeleton-card-text skeleton-shimmer" style="animation-delay: 0.1s;"></div>
                    <div class="skeleton-card-button skeleton-shimmer" style="animation-delay: 0.1s;"></div>
                </div>
                <div class="skeleton-card">
                    <div class="skeleton-card-icon skeleton-shimmer" style="animation-delay: 0.2s;"></div>
                    <div class="skeleton-card-title skeleton-shimmer" style="animation-delay: 0.2s;"></div>
                    <div class="skeleton-card-text skeleton-shimmer" style="animation-delay: 0.2s;"></div>
                    <div class="skeleton-card-button skeleton-shimmer" style="animation-delay: 0.2s;"></div>
                </div>
            </div>
            
            <!-- Chart Section -->
            <div class="skeleton-chart-container">
                <div style="width: 200px; height: 32px; margin: 0 auto;" class="skeleton-shimmer"></div>
                <div class="skeleton-chart skeleton-shimmer"></div>
            </div>
        `;
        
        this.skeletonContainer.innerHTML = skeletonHTML;
        document.body.insertBefore(this.skeletonContainer, document.body.firstChild);
    }
    
    simulateContentLoading() {
        // Simulate async operations
        Promise.all([
            this.loadWeb3(),
            this.loadChartData(),
            this.loadWalletInfo()
        ]).then(() => {
            this.ensureMinimumDisplayTime();
        }).catch(error => {
            console.error('Loading failed:', error);
            this.hideSkeleton(); // Still show app even if some features fail
        });
    }
    
    loadWeb3() {
        return new Promise(resolve => {
            setTimeout(() => {
                console.log('Web3 initialized');
                resolve();
            }, 800);
        });
    }
    
    loadChartData() {
        return new Promise(resolve => {
            setTimeout(() => {
                console.log('Chart data loaded');
                resolve();
            }, 1200);
        });
    }
    
    loadWalletInfo() {
        return new Promise(resolve => {
            setTimeout(() => {
                console.log('Wallet info loaded');
                resolve();
            }, 1000);
        });
    }
    
    ensureMinimumDisplayTime() {
        const elapsed = Date.now() - this.startTime;
        const remaining = this.minDisplayTime - elapsed;
        
        if (remaining > 0) {
            setTimeout(() => this.hideSkeleton(), remaining);
        } else {
            this.hideSkeleton();
        }
    }
    
    hideSkeleton() {
        // Add fade-out animation
        if (this.skeletonContainer) {
            this.skeletonContainer.classList.add('skeleton-fade-out');
        }
        
        // Show real app content after animation
        setTimeout(() => {
            if (this.skeletonContainer) {
                this.skeletonContainer.remove();
            }
            
            document.body.classList.remove('skeleton-loading');
            const realApp = document.getElementById('realApp');
            if (realApp) {
                realApp.style.display = 'block';
            }
            
            // Initialize the actual application
            if (typeof initRealApp === 'function') {
                initRealApp();
            }
            
            console.log('App fully loaded and ready');
        }, 500); // Match animation duration
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const skeletonLoader = new SkeletonLoader();
    skeletonLoader.init();
});