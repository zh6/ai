<template>
  <div class="sql-ai-container">
    <h2>自然语言转SQL查询</h2>
    <div class="input-container">
      <el-input
        v-model="naturalLanguage"
        type="textarea"
        :rows="4"
        placeholder="请输入自然语言描述，例如：查询所有年龄大于25岁的用户的姓名和邮箱"
      />
      <el-button type="primary" @click="convertToSQL" :loading="loading">
        转换为SQL
      </el-button>
    </div>
    
    <div v-if="sqlQuery" class="result-container">
      <h3>生成的SQL查询：</h3>
      <el-card class="sql-card">
        <pre><code>{{ sqlQuery }}</code></pre>
        <el-button size="small" @click="copySQL" style="margin-top: 10px">
          复制SQL
        </el-button>
      </el-card>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { convertNL2SQL } from '../services/aiService'

export default {
  name: 'SQLAI',
  setup() {
    const naturalLanguage = ref('')
    const sqlQuery = ref('')
    const loading = ref(false)

    const convertToSQL = async () => {
      if (!naturalLanguage.value.trim()) {
        ElMessage.warning('请输入自然语言描述')
        return
      }

      loading.value = true
      try {
        const response = await convertNL2SQL(naturalLanguage.value)
        sqlQuery.value = response.sql_query
        ElMessage.success('转换成功')
      } catch (error) {
        ElMessage.error(error.message || '转换失败，请重试')
      } finally {
        loading.value = false
      }
    }

    const copySQL = () => {
      navigator.clipboard.writeText(sqlQuery.value)
      ElMessage.success('SQL已复制到剪贴板')
    }

    return {
      naturalLanguage,
      sqlQuery,
      loading,
      convertToSQL,
      copySQL
    }
  }
}
</script>

<style scoped>
.sql-ai-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.input-container {
  margin: 20px 0;
}

.result-container {
  margin-top: 20px;
}

.sql-card {
  background-color: #f8f9fa;
}

pre {
  margin: 0;
  white-space: pre-wrap;
  word-wrap: break-word;
}

code {
  color: #476582;
  padding: 10px;
  display: block;
}

.el-button {
  margin-top: 10px;
}
</style> 