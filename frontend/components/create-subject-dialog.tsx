"use client"

import type React from "react"

import { useState } from "react"
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

interface CreateSubjectDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSubmit: (data: {
    name: string
    description?: string
    semester?: string
    teacher_name?: string
  }) => Promise<void>
}

export default function CreateSubjectDialog({ open, onOpenChange, onSubmit }: CreateSubjectDialogProps) {
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [semester, setSemester] = useState("")
  const [teacherName, setTeacherName] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

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
    if (!name.trim()) return

    setLoading(true)
    setError("")

    try {
      await onSubmit({
        name: name.trim(),
        description: description.trim() || undefined,
        semester: semester.trim() || undefined,
        teacher_name: teacherName.trim() || undefined,
      })
      // Reset form
      setName("")
      setDescription("")
      setSemester("")
      setTeacherName("")
    } catch (error: any) {
      const errorMessage = getErrorMessage(error)
      setError(errorMessage)
      console.error("Failed to create subject:", error)
    } finally {
      setLoading(false)
    }
  }

  const handleOpenChange = (newOpen: boolean) => {
    if (!loading) {
      onOpenChange(newOpen)
      if (!newOpen) {
        // Reset form when closing
        setName("")
        setDescription("")
        setSemester("")
        setTeacherName("")
        setError("")
      }
    }
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Create New Subject</DialogTitle>
          <DialogDescription>Add a new subject to the system. Fill in the details below.</DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4 py-4 max-h-[60vh] overflow-y-auto">
            {error && (
              <Alert variant="destructive">
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="grid gap-2">
              <Label htmlFor="name">Subject Name *</Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g., Mathematics, Computer Science"
                required
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Brief description of the subject (optional)"
                rows={3}
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="semester">Semester</Label>
              <Input
                id="semester"
                value={semester}
                onChange={(e) => setSemester(e.target.value)}
                placeholder="e.g., Winter 2024, Spring 2025"
              />
            </div>

            <div className="grid gap-2">
              <Label htmlFor="teacher_name">Teacher Name</Label>
              <Input
                id="teacher_name"
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
                  Creating...
                </>
              ) : (
                "Create Subject"
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
