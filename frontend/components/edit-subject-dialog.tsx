"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2 } from "lucide-react"

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

interface EditSubjectDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  subject: Subject | null
  onSubmit: (data: {
    name: string
    description?: string
    semester?: string
    teacher_name?: string
  }) => Promise<void>
}

export default function EditSubjectDialog({ open, onOpenChange, subject, onSubmit }: EditSubjectDialogProps) {
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [semester, setSemester] = useState("")
  const [teacherName, setTeacherName] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    if (subject) {
      setName(subject.name)
      setDescription(subject.description || "")
      setSemester(subject.semester || "")
      setTeacherName(subject.teacher_name || "")
      setError("") // Clear any previous errors
    }
  }, [subject])

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

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!name.trim() || !subject) return

    setLoading(true)
    setError("")

    try {
      await onSubmit({
        name: name.trim(),
        description: description.trim() || undefined,
        semester: semester.trim() || undefined,
        teacher_name: teacherName.trim() || undefined,
      })
    } catch (error: any) {
      const errorMessage = getErrorMessage(error)
      setError(errorMessage)
      console.error("Failed to update subject:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenChange = (newOpen: boolean) => {
    if (!loading) {
      onOpenChange(newOpen)
      if (!newOpen) {
        setError("") // Clear errors when closing
      }
    }
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Edit Subject</DialogTitle>
          <DialogDescription>Update the subject details. Changes will be saved to the database.</DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4 max-h-[60vh] overflow-y-auto">
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="grid gap-2">
              <Label htmlFor="edit-name">Subject Name *</Label>
              <Input
                id="edit-name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g., Mathematics, Computer Science"
                required
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="edit-description">Description</Label>
              <Textarea
                id="edit-description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Brief description of the subject (optional)"
                rows={3}
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="edit-semester">Semester</Label>
              <Input
                id="edit-semester"
                value={semester}
                onChange={(e) => setSemester(e.target.value)}
                placeholder="e.g., Winter 2024, Spring 2025"
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="edit-teacher_name">Teacher Name</Label>
              <Input
                id="edit-teacher_name"
                value={teacherName}
                onChange={(e) => setTeacherName(e.target.value)}
                placeholder="e.g., Prof. Dr. Smith"
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => handleOpenChange(false)} disabled={loading}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading || !name.trim()}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Updating...
                </>
              ) : (
                "Update Subject"
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
