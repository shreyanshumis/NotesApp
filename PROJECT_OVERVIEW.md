# Scribe NotesApp — Project Overview

## What is Scribe?

Scribe is a personal notes app designed to feel like a private digital journal.

The goal of the app is to give users a quiet, elegant place to write, organize, search, and export their thoughts. Instead of feeling like a plain notes tool, Scribe uses a warm journal-inspired design with soft colors, serif typography, subtle motion, and a calm writing experience.

The app is intended for users who want a simple private space for notes, reflections, ideas, reminders, or short pieces of writing.

## What the app is intended to do

Scribe allows a user to:

- Sign in securely with Google
- Create personal notes
- View only their own notes
- Edit existing notes
- Delete notes they no longer need
- Search through their notes
- Share or export a note as an image or PDF
- Use the app in light or dark mode

The main idea is privacy and simplicity: every user gets their own journal, and they should not see anyone else’s notes.

## User Flow

### 1. Opening the app

When a user opens Scribe, they are taken to the app’s journal experience.

If they are not logged in, they are asked to sign in before accessing their notes.

### 2. Signing in

The user signs in using Google.

After login, the app connects their notes to their account, so their journal remains private.

### 3. Viewing the journal

After signing in, the user sees their personal journal page.

This page shows:

- A search bar
- A button to create a new note
- A grid/list of their saved notes
- An empty state if they have not written anything yet

### 4. Creating a note

The user clicks the new note button and writes:

- A title
- The note content

After saving, the note is stored and shown in their journal.

### 5. Searching notes

The user can search their journal using keywords.

The app searches through note titles and note content to help the user find older entries quickly.

### 6. Viewing a note

When the user opens a note, they can read it in a clean detail view.

The note detail page focuses on readability, with actions placed separately so the writing remains the main focus.

### 7. Editing or deleting

From the note detail page, the user can:

- Edit the note
- Delete the note

These actions only affect the notes owned by that user.

### 8. Sharing or exporting

The user can export a note as:

- PDF
- Image

This makes it easy to save a note outside the app or share it with someone else.

## Design Direction

The design language is inspired by:

- Leather-bound journals
- Premium paper
- Soft royal colors
- Calm writing apps
- Minimal private workspaces

The interface uses:

- Warm ivory backgrounds
- Muted purple accents
- Antique gold details
- Serif headings
- Soft shadows
- Gentle background animations
- Dark mode support

The app avoids harsh colors and loud animations. The experience is meant to feel quiet, personal, and polished.

## Privacy Approach

Scribe is built around personal ownership.

Each note belongs to the user who created it. A logged-in user can only see and manage their own notes.

This means:

- User A cannot view User B’s notes
- User A cannot edit User B’s notes
- User A cannot export User B’s notes

The app is intended to behave like a private journal for each account.

## Technologies Used — High Level

Scribe is built with:

- Django for the main web application
- Python for backend logic
- Google login for authentication
- A database for storing users and notes
- HTML templates for the pages
- CSS and JavaScript for styling, theme switching, and interface behavior
- PDF/image generation tools for exporting notes
- Render for deployment

In simple terms:

- Django runs the app
- Google handles sign-in
- The database stores notes
- The frontend creates the journal-like experience
- Render hosts the project online

## Deployment Goal

The app is intended to be deployed online so users can access it through a browser.

Render is used as the hosting platform. The deployed version connects to an online database and serves the app publicly.

## Future Improvements

Possible future additions include:

- Rich text editor for longer notes
- Tags or folders
- Favorite notes
- Note pinning
- Better mobile writing experience
- Public share links
- Account settings page
- More export customization

## Summary

Scribe NotesApp is a private journal-style notes application.

It is meant to help users write and manage personal notes in a calm, elegant, and secure space. The focus is on privacy, simplicity, readability, and a polished user experience.
