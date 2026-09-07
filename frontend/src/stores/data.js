import { defineStore } from 'pinia'
import { apiFetch, TASK_API } from '../api'

export const useDataStore = defineStore('data', {
  state: () => ({
    employees: [],
    tasks: [],
    busyEmployees: [],
    importantTasks: [],
    selectedEmployeeId: null,
    selectedTaskId: null,
    loading: false,
    error: ''
  }),
  getters: {
    selectedEmployee: (state) =>
      state.employees.find((e) => e.id === state.selectedEmployeeId) || null,
    selectedTask: (state) =>
      state.tasks.find((t) => t.id === state.selectedTaskId) || null,
    filteredTasks: (state) =>
      state.selectedEmployeeId
        ? state.tasks.filter((t) => t.assignee === state.selectedEmployeeId)
        : state.tasks
  },
  actions: {
    selectEmployee(id) {
      this.selectedEmployeeId = this.selectedEmployeeId === id ? null : id
      this.selectedTaskId = null
    },
    selectTask(id) {
      this.selectedTaskId = this.selectedTaskId === id ? null : id
    },
    async run(fn) {
      this.loading = true
      this.error = ''
      try {
        await fn()
      } catch (e) {
        this.error = e.message
      } finally {
        this.loading = false
      }
    },
    async fetchEmployees() {
      await this.run(async () => {
        this.employees = await apiFetch(TASK_API, '/api/employees/')
      })
    },
    async fetchTasks() {
      await this.run(async () => {
        this.tasks = await apiFetch(TASK_API, '/api/tasks/')
      })
    },
    async fetchBusyEmployees() {
      await this.run(async () => {
        this.busyEmployees = await apiFetch(TASK_API, '/api/employees/busy/')
      })
    },
    async fetchImportantTasks() {
      await this.run(async () => {
        this.importantTasks = await apiFetch(TASK_API, '/api/tasks/important/')
      })
    },
    async refresh() {
      await this.run(async () => {
        ;[this.employees, this.tasks] = await Promise.all([
          apiFetch(TASK_API, '/api/employees/'),
          apiFetch(TASK_API, '/api/tasks/')
        ])
      })
    },
    async createEmployee(payload) {
      await apiFetch(TASK_API, '/api/employees/', {
        method: 'POST',
        body: payload
      })
      await this.fetchEmployees()
    },
    async createTask(payload) {
      await apiFetch(TASK_API, '/api/tasks/', {
        method: 'POST',
        body: payload
      })
      await this.fetchTasks()
    },
    async updateTaskStatus(taskId, status) {
      await apiFetch(TASK_API, `/api/tasks/${taskId}/`, {
        method: 'PATCH',
        body: { status }
      })
      await this.fetchTasks()
    }
  }
})
