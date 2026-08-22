# Proyecto

Estructura profesional y modular preparada para el desarrollo asistido por IA, documentación técnica, seguimiento de metodología y automatización CI/CD.

## 📁 Estructura del Repositorio

```text
.
├── .agents/                    # Directivas, reglas y flujos para Agentes de IA
│   ├── AGENTS.md               # Directivas globales del espacio de trabajo
│   ├── rules/                  # Reglas específicas de desarrollo y documentación
│   └── workflows/              # Flujos de trabajo automatizados para el agente
├── .github/                    # Configuración de GitHub
│   └── workflows/              # Acciones automatizadas (CI/CD Workflows)
├── docs/                       # Documentación del Proyecto
│   ├── tecnica/                # Arquitectura, APIs, instalación y guías dev
│   ├── metodologia/            # Seguimiento de sprints, backlog y metodología
│   ├── pruebas/                # Planes de pruebas, casos de uso y reportes QA
│   └── usuarios/               # Manuales de usuario, guías y documentación final
├── obsidian/                   # Vault de Obsidian (Documentación interna para la IA)
│   ├── Index.md                # Índice maestro del vault
│   ├── Bitacora/               # Registro de cambios diario (YYYY-MM-DD.md)
│   ├── Arquitectura/           # Diagramas y diseño de componentes
│   ├── Modulos/                # Detalles de módulos e integraciones
│   └── Contexto/               # Contexto persistente del dominio para el Agente
├── requirements/               # Especificaciones y Requerimientos del Proyecto
│   ├── funcionales/            # Historias de usuario y requerimientos funcionales
│   └── tecnicos/               # Requisitos técnicos, dependencias e insumos
├── .gitignore                  # Archivos ignorados por Git
└── README.md                   # Descripción general del repositorio
```

---

## 🚀 Guía Rápida

- **Para subir Requerimientos:** Coloca tus documentos de especificaciones, archivos de requisitos e insumos en la carpeta [`requirements/`](file:///d:/ernestofm/Proyecto/requirements).
- **Para Consultar Documentación:** Revisa la carpeta [`docs/`](file:///d:/ernestofm/Proyecto/docs).
- **Para el Agente de IA:** El agente utiliza la carpeta [`.agents/`](file:///d:/ernestofm/Proyecto/.agents) y actualiza automáticamente la bitácora e índice en [`obsidian/`](file:///d:/ernestofm/Proyecto/obsidian).
