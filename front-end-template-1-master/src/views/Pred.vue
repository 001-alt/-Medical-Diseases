<!-- <template>
  <div class="pred-container">
    <div class="left-section">
      <div class="header">
        <img src="../assets/logo.png" class="logo" alt="Logo">
        <h1 class="app-title">医疗疾病预测</h1>
      </div>

      <div class="input-section">
        <div class="input-group">
          <label class="input-label">输入文本内容</label>
          <div class="input-wrapper">
            <textarea v-model="inputText" class="text-input" placeholder="请输入您要分析的文本..." rows="5"
              @keydown.enter.prevent="submitModel"></textarea>
          </div>
        </div>

        <button @click="submitModel" :disabled="loading" class="predict-button">
          <span v-if="!loading">开始预测</span>
          <span v-else class="loading-indicator">
            <span class="spinner"></span>
            预测中...
          </span>
        </button>
      </div>
    </div>

    <div class="right-section">
      <div class="result-card">
        <div class="card-header">
          <h2>预测结果</h2>
          <div class="card-icon">
            <i class="icon-circle" v-if="result"></i>
          </div>
        </div>

        <div class="card-content">
          <div v-if="result" class="result-text">
            {{ result }}
          </div>
          <div v-else class="empty-state">
            <div class="empty-icon">🔮</div>
            <p>预测结果将显示在这里</p>
          </div>
        </div>
      </div>

      <div class="details-card">
        <div class="card-header">
          <h2>输入内容</h2>
        </div>

        <div class="card-content">
          <div v-if="inputText" class="analysis-details">
            <div class="detail-item">
              <span class="detail-label">用户输入:</span>
              <span class="detail-value">{{ inputText }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">预测结果:</span>
              <span class="detail-value">{{ result }}</span>
            </div>
          </div>
          <div v-else class="empty-state">
            <div class="empty-icon">📊</div>
            <p>没有输入内容</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PredictionApp',
  data() {
    return {
      inputText: '',
      result: '',
      loading: false,
    };
  },
  methods: {
    async submitModel() {
      if (!this.inputText.trim()) {
        this.result = '请输入有效内容';
        return;
      }

      this.loading = true;
      this.result = '';

      try {
        const response = await axios.post('/api/submitModel', {
          content: this.inputText,
        });

        if (response.data.code === 200) {
          this.result = response.data.data.resultData;
        } else {
          this.result = '预测失败: ' + response.data.message;
        }
      } catch (error) {
        console.error('API请求错误:', error);
        this.result = '预测服务暂时不可用';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style lang="less" scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

.pred-container {
  display: flex;
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  color: #ffffff;
  overflow: hidden;
}

.left-section {
  width: 40%;
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(10px);
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 3rem;
}

.logo {
  width: 60px;
  height: 60px;
  margin-right: 15px;
}

.app-title {
  font-weight: 600;
  font-size: 1.8rem;
  background: linear-gradient(90deg, #ffffff, #38bdf8);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.input-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.input-group {
  margin-bottom: 2rem;
}

.input-label {
  display: block;
  margin-bottom: 0.8rem;
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.7);
  font-weight: 500;
}

.input-wrapper {
  position: relative;
}

.text-input {
  width: 100%;
  padding: 1rem 1.2rem;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  background: rgba(30, 41, 59, 0.4);
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
  resize: none;

  &:focus {
    outline: none;
    border-color: #38bdf8;
    box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.3);
  }

  &::placeholder {
    color: rgba(255, 255, 255, 0.4);
  }
}

.predict-button {
  width: 100%;
  padding: 1rem;
  border: none;
  border-radius: 12px;
  background: linear-gradient(90deg, #3b82f6, #6366f1);
  color: white;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 50px;

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px -10px rgba(59, 130, 246, 0.6);
  }

  &:active:not(:disabled) {
    transform: translateY(0);
  }

  &:disabled {
    background: linear-gradient(90deg, #64748b, #475569);
    cursor: not-allowed;
    opacity: 0.7;
  }
}

.loading-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner {
  width: 1rem;
  height: 1rem;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

.right-section {
  flex: 1;
  padding: 2.5rem;
  display: grid;
  grid-template-rows: 1fr 1fr;
  gap: 1.5rem;
}

.result-card,
.details-card {
  background: rgba(15, 23, 42, 0.7);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  transition: transform 0.3s ease;

  &:hover {
    transform: translateY(-5px);
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.card-header h2 {
  font-size: 1.3rem;
  font-weight: 600;
  color: white;
}

.card-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-circle {
  display: block;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #10b981;
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.result-text {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #e2e8f0;
  background: linear-gradient(90deg, #f59e0b, #f97316);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-weight: 500;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: rgba(255, 255, 255, 0.6);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  opacity: 0.7;
}

.analysis-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
}

.detail-label {
  color: rgba(255, 255, 255, 0.7);
}

.detail-value {
  color: #38bdf8;
  font-weight: 500;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1024px) {
  .pred-container {
    flex-direction: column;
    height: auto;
    min-height: 100vh;
  }

  .left-section,
  .right-section {
    width: 100%;
    padding: 1.5rem;
  }

  .right-section {
    grid-template-rows: auto auto;
  }
}
</style> -->

<template>
  <div class="pred-container">
    <div class="left-section">
      <div class="header">
        <img src="../assets/logo.png" class="logo" alt="Logo">
        <h1 class="app-title">医疗疾病预测</h1>
      </div>

      <div class="input-section">
        <div class="input-group">
          <label class="input-label">输入文本内容</label>
          <div class="input-wrapper">
            <textarea v-model="inputText" class="text-input" placeholder="请输入您要分析的文本..." rows="5"
              @keydown.enter.prevent="submitModel"></textarea>
          </div>
        </div>

        <button @click="submitModel" :disabled="loading" class="predict-button">
          <span v-if="!loading">开始预测</span>
          <span v-else class="loading-indicator">
            <span class="spinner"></span>
            预测中...
          </span>
        </button>
      </div>
    </div>

    <div class="right-section">
      <div class="result-card">
        <div class="card-header">
          <h2>预测结果</h2>
          <div class="card-icon">
            <i class="icon-circle" v-if="result"></i>
          </div>
        </div>

        <div class="card-content">
          <div v-if="result" class="result-text">
            {{ result }}
          </div>
          <div v-else class="empty-state">
            <div class="empty-icon">🔮</div>
            <p>预测结果将显示在这里</p>
          </div>
        </div>
      </div>

      <div class="details-card">
        <div class="card-header">
          <h2>输入内容</h2>
        </div>

        <div class="card-content">
          <div v-if="inputText" class="analysis-details">
            <div class="detail-item">
              <span class="detail-label">用户输入:</span>
              <span class="detail-value">{{ inputText }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">预测结果:</span>
              <span class="detail-value">{{ result }}</span>
            </div>
          </div>
          <div v-else class="empty-state">
            <div class="empty-icon">📊</div>
            <p>没有输入内容</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'PredictionApp',
  data() {
    return {
      inputText: '',
      result: '',
      loading: false,
    };
  },
  methods: {
    async submitModel() {
      if (!this.inputText.trim()) {
        this.result = '请输入有效内容';
        return;
      }

      this.loading = true;
      this.result = '';

      try {
        const response = await axios.post('/api/submitModel', {
          content: this.inputText,
        });

        if (response.data.code === 200) {
          this.result = response.data.data.resultData;
        } else {
          this.result = '预测失败: ' + response.data.message;
        }
      } catch (error) {
        console.error('API请求错误:', error);
        this.result = '预测服务暂时不可用';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style lang="less" scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}

.pred-container {
  display: grid;
  grid-template-columns: 40% 60%;
  min-height: 100vh;
  background: linear-gradient(to bottom right, #000b1f, #001233, #001845);
  color: #e2e8f0;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    width: 100%;
    height: 100%;
    background:
      radial-gradient(circle at 20% 35%, rgba(5, 134, 255, 0.05) 0%, transparent 50%),
      radial-gradient(circle at 75% 44%, rgba(5, 134, 255, 0.05) 0%, transparent 40%);
    pointer-events: none;
  }
}

.left-section {
  background: rgba(2, 17, 43, 0.7);
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(59, 130, 246, 0.1);
  padding: 2.5rem;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;

  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(45deg,
        transparent 0%,
        rgba(59, 130, 246, 0.03) 50%,
        transparent 100%);
    animation: shine 8s infinite linear;
  }
}

.header {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  margin-bottom: 2.5rem;
}

.logo {
  width: 50px;
  height: 50px;
  margin-right: 1rem;
  filter: drop-shadow(0 0 8px rgba(59, 130, 246, 0.3));
}

.app-title {
  font-size: 2.2rem;
  font-weight: 700;
  background: linear-gradient(90deg, #60a5fa, #3b82f6);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 30px rgba(59, 130, 246, 0.3);
}

.input-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
  z-index: 1;
}

.input-group {
  margin-bottom: 2rem;
}

.input-label {
  display: block;
  margin-bottom: 1rem;
  color: rgba(226, 232, 240, 0.8);
  font-size: 1.1rem;
  font-weight: 500;
}

.input-wrapper {
  position: relative;
}

.text-input {
  width: 100%;
  background: rgba(2, 17, 43, 0.8);
  border: 1px solid rgba(59, 130, 246, 0.2);
  border-radius: 12px;
  padding: 1.5rem;
  color: #e2e8f0;
  font-size: 1.1rem;
  line-height: 1.7;
  height: 180px;
  transition: all 0.3s ease;
  resize: none;

  &:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2),
      0 0 20px rgba(59, 130, 246, 0.1);
  }

  &::placeholder {
    color: rgba(226, 232, 240, 0.4);
  }
}

.predict-button {
  width: 100%;
  height: 56px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border: none;
  border-radius: 12px;
  color: white;
  font-size: 1.1rem;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg,
        transparent,
        rgba(255, 255, 255, 0.2),
        transparent);
    transition: 0.5s;
  }

  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 12px 24px -8px rgba(59, 130, 246, 0.4);

    &::before {
      left: 100%;
    }
  }

  &:disabled {
    background: linear-gradient(90deg, #475569, #1e293b);
    cursor: not-allowed;
    opacity: 0.7;
  }
}

.loading-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
}

.spinner {
  width: 1.2rem;
  height: 1.2rem;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}

.right-section {
  padding: 2.5rem;
  display: grid;
  grid-template-rows: repeat(2, 1fr);
  gap: 2.5rem;
  position: relative;
  z-index: 1;
}

.result-card,
.details-card {
  background: rgba(2, 17, 43, 0.7);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 16px;
  padding: 2rem;
  position: relative;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg,
        transparent,
        rgba(59, 130, 246, 0.3),
        transparent);
  }

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 24px -8px rgba(0, 0, 0, 0.3);
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(59, 130, 246, 0.1);
}

.card-header h2 {
  color: #60a5fa;
  font-size: 1.5rem;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.card-icon {
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-circle {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #10b981;
  box-shadow: 0 0 12px rgba(16, 185, 129, 0.4);
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.result-text {
  background: linear-gradient(90deg, #60a5fa, #3b82f6);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  font-size: 1.4rem;
  line-height: 1.8;
  padding: 1rem 0;
  font-weight: 500;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: rgba(226, 232, 240, 0.6);
  text-align: center;
  padding: 3rem 2rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #60a5fa, #3b82f6);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.analysis-details {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1rem;
  background: rgba(2, 17, 43, 0.4);
  border-radius: 8px;
  border: 1px solid rgba(59, 130, 246, 0.1);
}

.detail-label {
  color: rgba(226, 232, 240, 0.7);
  font-weight: 500;
}

.detail-value {
  color: #60a5fa;
  font-weight: 500;
  text-align: right;
  flex: 1;
  margin-left: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes shine {
  from {
    transform: translateX(-100%);
  }

  to {
    transform: translateX(100%);
  }
}

@media (max-width: 1024px) {
  .pred-container {
    grid-template-columns: 1fr;
    height: auto;
    min-height: 100vh;
  }

  .left-section {
    border-right: none;
    border-bottom: 1px solid rgba(59, 130, 246, 0.1);
  }

  .right-section {
    padding: 1.5rem;
    grid-template-rows: auto auto;
    gap: 1.5rem;
  }

  .app-title {
    font-size: 1.8rem;
  }

  .text-input {
    height: 150px;
  }

  .result-text {
    font-size: 1.2rem;
  }
}

@media (max-width: 640px) {
  .pred-container {
    padding: 1rem;
  }

  .left-section,
  .right-section {
    padding: 1rem;
  }

  .header {
    margin-bottom: 1.5rem;
  }

  .logo {
    width: 40px;
    height: 40px;
  }

  .app-title {
    font-size: 1.5rem;
  }

  .card-header h2 {
    font-size: 1.3rem;
  }

  .result-text {
    font-size: 1.1rem;
  }

  .detail-item {
    flex-direction: column;
    gap: 0.5rem;
  }

  .detail-value {
    margin-left: 0;
    text-align: left;
  }
}
</style>
