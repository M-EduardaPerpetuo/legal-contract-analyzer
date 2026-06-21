import { useState } from 'react'
import './App.css'

function App() {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setFile(e.dataTransfer.files[0]);
      setResult(null); // Limpa o resultado anterior ao enviar novo arquivo
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      setResult(null);
    }
  };

  const handleAnalyze = async () => {
    if (!file) return;
    
    setIsLoading(true);
    setResult(null);

    // Encapsula o arquivo no formato esperado pelo FastAPI
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Ajuste a URL para a porta correta onde o FastAPI estiver rodando
      const response = await fetch('http://localhost:8000/api/v1/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Falha na comunicação com o servidor');
      }

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Erro técnico:", error);
      setResult({ error: "Não foi possível analisar o contrato. Verifique se o servidor FastAPI está rodando." });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>S.A.C. Auditoria</h1>
        <p>Análise de Risco em Contratos Jurídicos via IA</p>
      </header>

      <main className="app-main">
        <section 
          className={`drop-zone ${isDragging ? 'dragging' : ''}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <div className="drop-content">
            <span className="icon">📄</span>
            <h2>Arraste e solte o contrato aqui</h2>
            <p>ou</p>
            <label className="upload-btn">
              Selecione o arquivo
              <input 
                type="file" 
                accept=".pdf,.docx,.xlsx" 
                onChange={handleFileChange}
                hidden
              />
            </label>
            <p className="file-formats">Formatos suportados: PDF, DOCX, XLSX</p>
          </div>
        </section>

        {file && (
          <div className="file-info">
            <p><strong>Arquivo selecionado:</strong> {file.name}</p>
            <button 
              className="analyze-btn" 
              onClick={handleAnalyze}
              disabled={isLoading}
            >
              {isLoading ? 'Analisando com IA...' : 'Iniciar Auditoria por IA'}
            </button>
          </div>
        )}

        {result && (
          <div className="result-panel fade-in">
            {result.erro || result.error ? (
              <p className="error-text">{result.erro || result.error}</p>
            ) : (
              <>
                <div className="result-header">
                  <h3>Parecer Jurídico Final</h3>
                  <div className={`risk-badge risk-${result.nivel_de_risco}`}>
                    Nível de Risco: {result.nivel_de_risco}/5
                  </div>
                </div>
                
                <div className="result-content formatted-result">
                  <div className="result-section">
                    <h4>Resumo Executivo</h4>
                    <p>{result.resumo_executivo}</p>
                  </div>
                  
                  <div className="result-section warning-section">
                    <h4>Análise Detalhada e Mitigação</h4>
                    <p>{result.parecer_sugerido}</p>
                  </div>
                </div>
              </>
            )}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;