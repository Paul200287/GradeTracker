"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Input } from "@/components/ui/input"
import { Loader2, LogOut, RefreshCw, Plus, Search, Edit } from "lucide-react"
import UserProfile from "@/components/user-profile"
import CreateSubjectDialog from "@/components/create-subject-dialog"
import EditSubjectDialog from "@/components/edit-subject-dialog"
import { subjectApi } from "@/lib/api"

interface Subject {
  id: number
  name: string
  description?: string
  semester?: string
  teacher_name?: string
  user_id: number
  created_at: string
  updated_at: string
}

export default function SubjectsPage() {
  const [subjects, setSubjects] = useState<Subject[]>([])
  const [filteredSubjects, setFilteredSubjects] = useState<Subject[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")
  const [searchTerm, setSearchTerm] = useState("")
  const [currentUser, setCurrentUser] = useState<any>(null)
  const [createDialogOpen, setCreateDialogOpen] = useState(false)
  const [editDialogOpen, setEditDialogOpen] = useState(false)
  const [selectedSubject, setSelectedSubject] = useState<Subject | null>(null)
  const router = useRouter()

  useEffect(() => {
    // Check authentication
    const token = localStorage.getItem("jwt_token")
    const userData = localStorage.getItem("user_data")

    if (!token) {
      router.push("/")
      return
    }

    if (userData) {
      setCurrentUser(JSON.parse(userData))
    }

    fetchSubjects()
  }, [router])

  useEffect(() => {
    // Filter subjects based on search term
    const filtered = subjects.filter(
      (subject) =>
        subject.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (subject.description && subject.description.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (subject.semester && subject.semester.toLowerCase().includes(searchTerm.toLowerCase())) ||
        (subject.teacher_name && subject.teacher_name.toLowerCase().includes(searchTerm.toLowerCase())),
    )
    setFilteredSubjects(filtered)
  }, [subjects, searchTerm])

  const fetchSubjects = async () => {
    setLoading(true)
    setError("")

    try {
      const data = await subjectApi.getAll()
      setSubjects(data)
    } catch (err: any) {
      if (err.response?.status === 401) {
        setError("Session expired. Please login again.")
        setTimeout(() => handleLogout(), 2000)
      } else {
        const errorMessage = getErrorMessage(err)
        setError(errorMessage)
      }
    } finally {
      setLoading(false)
    }
  }

  const getErrorMessage = (error: any): string => {
    if (typeof error === "string") {
      return error
    }

    if (error?.response?.data) {
      const data = error.response.data

      // Handle FastAPI validation errors
      if (Array.isArray(data.detail)) {
        return data.detail.map((err: any) => `${err.loc?.join(".")}: ${err.msg}`).join(", ")
      }

      // Handle simple detail message
      if (typeof data.detail === "string") {
        return data.detail
      }

      // Handle other error formats
      if (data.message) {
        return data.message
      }
    }

    if (error?.message) {
      return error.message
    }

    return "An unexpected error occurred"
  }

  const handleLogout = () => {
    localStorage.removeItem("jwt_token")
    localStorage.removeItem("user_data")
    router.push("/")
  }

  const handleCreateSubject = async (subjectData: {
    name: string
    description?: string
    semester?: string
    teacher_name?: string
  }) => {
    try {
      await subjectApi.create(subjectData)
      setCreateDialogOpen(false)
      setError("") // Clear any previous errors
      fetchSubjects() // Refresh the list
    } catch (err: any) {
      const errorMessage = getErrorMessage(err)
      setError(`Failed to create subject: ${errorMessage}`)
    }
  }

  const handleEditSubject = async (subjectData: {
    name: string
    description?: string
    semester?: string
    teacher_name?: string
  }) => {
    if (!selectedSubject) return

    try {
      await subjectApi.update(selectedSubject.id, subjectData)
      setEditDialogOpen(false)
      setSelectedSubject(null)
      setError("") // Clear any previous errors
      fetchSubjects() // Refresh the list
    } catch (err: any) {
      const errorMessage = getErrorMessage(err)
      setError(`Failed to update subject: ${errorMessage}`)
    }
  }

  const handleRowClick = (subject: Subject) => {
    setSelectedSubject(subject)
    setEditDialogOpen(true)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
  }

  if (loading && subjects.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <Loader2 className="h-8 w-8 animate-spin mx-auto mb-4" />
          <p>Loading subjects...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold">Subjects Management</h1>
            {currentUser && (
              <p className="text-gray-600 mt-1">Welcome back, {currentUser.username || currentUser.email}</p>
            )}
          </div>
          <div className="flex gap-2">
            <Button variant="outline" onClick={fetchSubjects} disabled={loading}>
              <RefreshCw className={`h-4 w-4 mr-2 ${loading ? "animate-spin" : ""}`} />
              Refresh
            </Button>
            <Button variant="outline" onClick={handleLogout}>
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>

        <UserProfile />

        <Card>
          <CardHeader>
            <div className="flex justify-between items-center">
              <div>
                <CardTitle>All Subjects</CardTitle>
                <CardDescription>Manage and view all subjects in the system</CardDescription>
              </div>
              <Button onClick={() => setCreateDialogOpen(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Create new entry
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            {error && (
              <Alert variant="destructive" className="mb-4">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            {/* Search Field */}
            <div className="relative mb-4">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
              <Input
                placeholder="Search subjects by name, description, semester, or teacher..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>

            {filteredSubjects.length === 0 && !loading ? (
              <div className="text-center py-8">
                <p className="text-gray-500">
                  {searchTerm ? "No subjects found matching your search" : "No subjects found"}
                </p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>ID</TableHead>
                      <TableHead>Name</TableHead>
                      <TableHead>Description</TableHead>
                      <TableHead>Semester</TableHead>
                      <TableHead>Teacher</TableHead>
                      <TableHead>User ID</TableHead>
                      <TableHead>Created</TableHead>
                      <TableHead>Updated</TableHead>
                      <TableHead>Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredSubjects.map((subject) => (
                      <TableRow
                        key={`subject-${subject.id}`}
                        className="cursor-pointer hover:bg-gray-50"
                        onClick={() => handleRowClick(subject)}
                      >
                        <TableCell className="font-medium">{subject.id}</TableCell>
                        <TableCell className="font-medium">{subject.name}</TableCell>
                        <TableCell>{subject.description || "-"}</TableCell>
                        <TableCell>{subject.semester || "-"}</TableCell>
                        <TableCell>{subject.teacher_name || "-"}</TableCell>
                        <TableCell>{subject.user_id}</TableCell>
                        <TableCell>{formatDate(subject.created_at)}</TableCell>
                        <TableCell>{formatDate(subject.updated_at)}</TableCell>
                        <TableCell>
                          <Button
                            key={`edit-${subject.id}`}
                            variant="ghost"
                            size="sm"
                            onClick={(e) => {
                              e.stopPropagation()
                              handleRowClick(subject)
                            }}
                          >
                            <Edit className="h-4 w-4" />
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Create Subject Dialog */}
        <CreateSubjectDialog
          open={createDialogOpen}
          onOpenChange={setCreateDialogOpen}
          onSubmit={handleCreateSubject}
        />

        {/* Edit Subject Dialog */}
        <EditSubjectDialog
          open={editDialogOpen}
          onOpenChange={setEditDialogOpen}
          subject={selectedSubject}
          onSubmit={handleEditSubject}
        />
      </div>
    </div>
  )
}
