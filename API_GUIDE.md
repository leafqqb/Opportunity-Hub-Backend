# Opportunity Hub — Frontend API Guide

> **Base URL (local):** `http://localhost:8000/api/`  
> **Auth scheme:** Token — send `Authorization: Token <your-token>` on every protected request.  
> **Pagination:** List endpoints return `{ count, next, previous, results[] }`. Use `?limit=20&offset=0`.

---

## Table of Contents

1. [Authentication Flow](#1-authentication-flow)
2. [Profile Endpoints](#2-profile-endpoints)
3. [Opportunities](#3-opportunities)
4. [Bookmarks](#4-bookmarks)
5. [Field Reference](#5-field-reference)
6. [Error Reference](#6-error-reference)
7. [Full Frontend Workflow](#7-full-frontend-workflow)
8. [Practical Code Snippets](#8-practical-code-snippets)

---

## 1. Authentication Flow

### 1.1 Pick a role first

Before registering, the user picks **Student** or **Organization** in your UI. This maps to the `role` field: `"student"` or `"company"`.

---

### 1.2 Register

`POST /api/auth/register/`  
**Auth required:** No

#### Student body
```json
{
  "username": "ahmad99",
  "email": "ahmad@example.com",
  "password": "StrongPass123!",
  "role": "student",
  "headline": "CS student at KAU",
  "bio": "Looking for internships in AI.",
  "location": "Jeddah, Saudi Arabia",
  "university": "King Abdulaziz University",
  "graduation_year": 2026,
  "major": "Computer Science",
  "skills": "Python,Machine Learning,SQL"
}
```

#### Organization body
```json
{
  "username": "aramco_hr",
  "email": "hr@aramco.com",
  "password": "StrongPass123!",
  "role": "company",
  "company_name": "Saudi Aramco",
  "industry": "Energy",
  "bio": "One of the world's largest energy companies.",
  "location": "Dhahran, Saudi Arabia",
  "website": "https://www.aramco.com"
}
```

> ⚠️ `company_name` is **required** when `role` is `"company"`. Registration will fail without it.

#### Response `201 Created`
```json
{
  "token": "9944b09199c62dcf37f44568109b6bc19df8f37a",
  "user": {
    "id": 1,
    "username": "ahmad99",
    "email": "ahmad@example.com",
    "role": "student"
  }
}
```

**Save the token immediately.** It's the user's session key.

---

### 1.3 Login

`POST /api/auth/login/`  
**Auth required:** No

Log in with **username** or **email** — either works.

```json
{ "username": "ahmad99", "password": "StrongPass123!" }
```
```json
{ "email": "ahmad@example.com", "password": "StrongPass123!" }
```

#### Response `200 OK` — same shape as register
```json
{
  "token": "9944b09199c62dcf37f44568109b6bc19df8f37a",
  "user": { "id": 1, "username": "ahmad99", "email": "ahmad@example.com", "role": "student" }
}
```

---

### 1.4 Get current user

`GET /api/auth/me/`  
**Auth required:** Yes

Returns the full profile of whoever owns the token. Use this on page load to rehydrate session state.

---

### 1.5 Logout

`POST /api/auth/logout/`  
**Auth required:** Yes  
**Body:** none

Deletes the token server-side. After this, all requests using the old token return `401`. Clear the token from storage.

#### Response `200 OK`
```json
{ "detail": "Logged out successfully." }
```

---

### 1.6 Storing the token

```js
// After login or register:
localStorage.setItem('ohToken', data.token)
localStorage.setItem('ohUser', JSON.stringify(data.user))

// On every protected request:
const token = localStorage.getItem('ohToken')
headers: { 'Authorization': `Token ${token}` }

// On logout:
localStorage.removeItem('ohToken')
localStorage.removeItem('ohUser')
```

---

## 2. Profile Endpoints

### 2.1 View & edit your own profile

`GET /api/profiles/me/` — returns your full profile including email  
`PATCH /api/profiles/me/` — update any editable fields  
`DELETE /api/profiles/me/` — permanently delete account  
**Auth required:** Yes for all three

#### PATCH example (student)
```json
{
  "headline": "Final year CS student",
  "bio": "Passionate about NLP and open-source.",
  "location": "Riyadh, Saudi Arabia",
  "university": "KFUPM",
  "graduation_year": 2026,
  "major": "Software Engineering",
  "skills": "Python,Django,React"
}
```

#### PATCH example (company)
```json
{
  "headline": "Building Saudi Arabia's AI future",
  "bio": "We hire top engineering talent.",
  "company_name": "Saudi Aramco",
  "industry": "Energy",
  "location": "Dhahran, Saudi Arabia",
  "website": "https://www.aramco.com"
}
```

> ℹ️ `username`, `email`, and `role` are **read-only** — they cannot be changed after registration.

---

### 2.2 Public profile (read-only)

`GET /api/profiles/{username}/`  
**Auth required:** No

Returns the public fields of any user. Email is **not** included.

```
GET /api/profiles/ahmad99/
```

---

## 3. Opportunities

### 3.1 Browse opportunities (public)

`GET /api/opportunities/`  
**Auth required:** No

Returns a paginated list. Default page size is 20.

#### All filter parameters

| Param | Type | Example | Notes |
|---|---|---|---|
| `search` | string | `?search=data+science` | Searches title, description, category, org name |
| `category` | string | `?category=engineering` | Partial match |
| `location` | string | `?location=riyadh` | Partial match |
| `type` | string | `?type=Internship` | Exact, case-insensitive |
| `organization` | string | `?organization=aramco` | Partial match |
| `major` | string | `?major=computer+science` | Partial match |
| `is_paid` | boolean | `?is_paid=true` | `true` or `false` |
| `is_urgent` | boolean | `?is_urgent=true` | `true` or `false` |
| `deadline_before` | date | `?deadline_before=2026-08-01` | YYYY-MM-DD, inclusive |
| `deadline_after` | date | `?deadline_after=2026-05-01` | YYYY-MM-DD, inclusive |
| `limit` | int | `?limit=10` | Pagination |
| `offset` | int | `?offset=20` | Pagination |

#### Combine filters freely
```
GET /api/opportunities/?search=ai&location=riyadh&is_paid=true&type=Internship
```

#### Response shape (list)
```json
{
  "count": 87,
  "next": "http://localhost:8000/api/opportunities/?limit=20&offset=20",
  "previous": null,
  "results": [
    {
      "id": 12,
      "title": "AI Research Internship",
      "organization_name": "KACST",
      "opportunity_type": "Internship",
      "category": "Artificial Intelligence",
      "location": "Riyadh, Saudi Arabia",
      "application_deadline": "2026-08-15",
      "is_paid": true,
      "is_urgent": false,
      "major": "Computer Science, Data Science",
      "external_url": "https://kacst.gov.sa/apply",
      "posted_by": "kacst_hr",
      "status": "active",
      "is_expired": false,
      "created_at": "2026-05-01T09:00:00Z"
    }
  ]
}
```

---

### 3.2 View a single opportunity

`GET /api/opportunities/{id}/`  
**Auth required:** No

Returns the full detail object with `responsibilities`, `requirements`, and `benefits`.

#### Response shape (detail)
```json
{
  "id": 12,
  "title": "AI Research Internship",
  "organization_name": "KACST",
  "description": "Join our AI lab for a 12-week research internship...",
  "opportunity_type": "Internship",
  "category": "Artificial Intelligence",
  "location": "Riyadh, Saudi Arabia",
  "external_url": "https://kacst.gov.sa/apply",
  "application_deadline": "2026-08-15",
  "is_paid": true,
  "is_urgent": false,
  "major": "Computer Science, Data Science",
  "responsibilities": "Conduct literature reviews\nBuild ML pipelines\nPresent findings weekly",
  "requirements": "GPA 3.5+\nFamiliarity with Python and PyTorch",
  "benefits": "Stipend: SAR 3,000/month\nHousing allowance\nCertificate",
  "is_active": true,
  "posted_by": "kacst_hr",
  "posted_by_id": 5,
  "status": "active",
  "is_expired": false,
  "created_at": "2026-05-01T09:00:00Z",
  "updated_at": "2026-05-01T09:00:00Z"
}
```

> ℹ️ **`status`** values: `"active"`, `"expired"`, `"inactive"`. Use `is_expired` or `status` to show a badge on the detail page.

> ℹ️ **Applying:** There are no in-app applications. The "Apply Now" button should open `external_url` in a new tab.

---

### 3.3 Create an opportunity

`POST /api/opportunities/`  
**Auth required:** Yes (any role)

#### Required fields
```json
{
  "title": "Summer UI/UX Internship",
  "organization_name": "TechCo SA",
  "description": "Join our design team for 10 weeks...",
  "opportunity_type": "Internship",
  "external_url": "https://techcosa.com/apply"
}
```

#### All optional fields
```json
{
  "category": "Design",
  "location": "Riyadh, Saudi Arabia",
  "application_deadline": "2026-07-31",
  "is_paid": true,
  "is_urgent": true,
  "major": "Design, Computer Science",
  "responsibilities": "Design wireframes\nConduct user testing",
  "requirements": "Figma proficiency\nNo experience required",
  "benefits": "Paid stipend\nMentorship\nCertificate"
}
```

#### Valid `opportunity_type` values
`"Internship"` · `"Scholarship"` · `"Competition"` · `"COOP"` · `"Bootcamp"` · `"Volunteering"` · `"Program"`

#### Response `201 Created` — full detail object

---

### 3.4 Update an opportunity

`PATCH /api/opportunities/{id}/` — partial update (recommended)  
`PUT /api/opportunities/{id}/` — full replace  
**Auth required:** Yes — **only the creator** can update

```json
{ "location": "Hybrid", "is_urgent": true }
```

#### Response `200 OK` — updated detail object

---

### 3.5 Delete an opportunity

`DELETE /api/opportunities/{id}/`  
**Auth required:** Yes — **only the creator** can delete

#### Response `204 No Content`

---

### 3.6 My posted opportunities

`GET /api/opportunities/mine/`  
**Auth required:** Yes

Returns all opportunities created by the logged-in user. **Not paginated** — returns a plain array.

Use this to populate the organization's dashboard table.

---

## 4. Bookmarks

> Only accounts with `role: "student"` can use bookmark endpoints. Company accounts will receive `403`.

### 4.1 Save a bookmark

`POST /api/bookmarks/`  
**Auth required:** Yes (student only)

```json
{ "opportunity_id": 12 }
```

#### Response `201 Created`
```json
{
  "id": 7,
  "user": "ahmad99",
  "opportunity": {
    "id": 12,
    "title": "AI Research Internship",
    "organization_name": "KACST",
    "opportunity_type": "Internship",
    "category": "Artificial Intelligence",
    "location": "Riyadh, Saudi Arabia",
    "application_deadline": "2026-08-15",
    "is_paid": true,
    "is_urgent": false,
    "major": "Computer Science, Data Science",
    "external_url": "https://kacst.gov.sa/apply",
    "posted_by": "kacst_hr",
    "status": "active",
    "is_expired": false,
    "created_at": "2026-05-01T09:00:00Z"
  },
  "created_at": "2026-05-15T14:00:00Z"
}
```

> ⚠️ Bookmarking the same opportunity twice returns `400`:  
> `{ "detail": "This opportunity is already bookmarked." }`

---

### 4.2 List bookmarks

`GET /api/bookmarks/`  
**Auth required:** Yes (student only)

Returns the logged-in student's bookmarks. **Sorted by nearest deadline** — ready for the Deadline Tracker UI.

Paginated: `{ count, next, previous, results[] }`

---

### 4.3 Remove a bookmark

`DELETE /api/bookmarks/{id}/`  
**Auth required:** Yes (student only)

`id` here is the **bookmark ID** (from the bookmark object), not the opportunity ID.

#### Response `204 No Content`

---

## 5. Field Reference

### Opportunity status logic

| `status` value | Meaning |
|---|---|
| `"active"` | Live and accepting interest |
| `"expired"` | Deadline has passed |
| `"inactive"` | Hidden by admin |

Use `status` or `is_expired: true` to show an "Expired" badge.

---

### User profile fields

| Field | Student | Company | Notes |
|---|---|---|---|
| `username` | ✅ | ✅ | Read-only after register |
| `email` | ✅ | ✅ | Read-only, only in own profile |
| `role` | `"student"` | `"company"` | Read-only |
| `headline` | ✅ | ✅ | Short tagline, max 140 chars |
| `bio` | ✅ | ✅ | Free text |
| `location` | ✅ | ✅ | |
| `website` | ✅ | ✅ | URL |
| `university` | ✅ | — | |
| `graduation_year` | ✅ | — | Integer e.g. `2026` |
| `major` | ✅ | — | |
| `skills` | ✅ | — | Comma-separated string |
| `company_name` | — | ✅ | Required at registration |
| `industry` | — | ✅ | |

---

## 6. Error Reference

### HTTP status codes

| Code | Meaning | Common cause |
|---|---|---|
| `200` | OK | Successful GET, PATCH |
| `201` | Created | Successful POST |
| `204` | No Content | Successful DELETE |
| `400` | Bad Request | Validation error, missing required field, duplicate bookmark |
| `401` | Unauthorized | Missing or invalid token |
| `403` | Forbidden | Authenticated but not allowed (wrong role, not owner) |
| `404` | Not Found | Resource doesn't exist or was deleted |

### Error body shapes

```json
// 401 — missing token
{ "detail": "Authentication credentials were not provided." }

// 403 — wrong role or not owner
{ "detail": "Only student accounts can perform this action." }

// 400 — validation
{ "organization_name": ["This field is required."] }
{ "email": ["A user with that email already exists."] }
{ "detail": "This opportunity is already bookmarked." }
```

---

## 7. Full Frontend Workflow

### Student journey
```
Landing page
  → Choose "Student" → Register (POST /auth/register/)
  → Save token + user in localStorage
  → Home: Browse opportunities (GET /opportunities/?...)
  → Click card → Detail page (GET /opportunities/{id}/)
  → "Apply Now" → opens external_url in new tab
  → "Bookmark" → POST /bookmarks/ { opportunity_id }
  → Bookmarks page → GET /bookmarks/ (sorted by deadline)
  → Remove bookmark → DELETE /bookmarks/{bookmark_id}/
  → Profile page → PATCH /profiles/me/
  → Logout → POST /auth/logout/
```

### Organization journey
```
Landing page
  → Choose "Organization" → Register (POST /auth/register/)
  → Save token + user in localStorage
  → Dashboard → GET /opportunities/mine/
  → "Post Opportunity" → POST /opportunities/
  → Edit row → PATCH /opportunities/{id}/
  → Delete row → DELETE /opportunities/{id}/
  → Profile page → PATCH /profiles/me/
  → Logout → POST /auth/logout/
```

---

## 8. Practical Code Snippets

### API client helper

```js
const BASE = 'http://localhost:8000/api'

function getToken() {
  return localStorage.getItem('ohToken')
}

async function api(path, { method = 'GET', body } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  const token = getToken()
  if (token) headers['Authorization'] = `Token ${token}`

  const res = await fetch(`${BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  })

  if (res.status === 204) return null
  const data = await res.json()
  if (!res.ok) throw data   // throw the error object for the caller to handle
  return data
}
```

---

### Register & login

```js
// Register
const { token, user } = await api('/auth/register/', {
  method: 'POST',
  body: { username: 'ahmad99', email: 'ahmad@example.com', password: 'Pass123!', role: 'student' }
})
localStorage.setItem('ohToken', token)
localStorage.setItem('ohUser', JSON.stringify(user))

// Login
const { token, user } = await api('/auth/login/', {
  method: 'POST',
  body: { email: 'ahmad@example.com', password: 'Pass123!' }
})
localStorage.setItem('ohToken', token)

// Logout
await api('/auth/logout/', { method: 'POST' })
localStorage.removeItem('ohToken')
localStorage.removeItem('ohUser')
```

---

### Browse & filter opportunities

```js
// Basic browse
const { results, count, next } = await api('/opportunities/?limit=20&offset=0')

// Filtered: paid internships in Riyadh matching "data"
const { results } = await api(
  '/opportunities/?search=data&type=Internship&location=riyadh&is_paid=true'
)

// Category tabs (All / Internships / Scholarships / ...)
const params = type !== 'All' ? `?type=${type}` : ''
const { results } = await api(`/opportunities/${params}`)
```

---

### Opportunity detail page

```js
const opportunity = await api('/opportunities/12/')

// Apply button
window.open(opportunity.external_url, '_blank', 'noopener,noreferrer')

// Expired badge
if (opportunity.is_expired || opportunity.status === 'expired') {
  // show red "Expired" tag
}
```

---

### Create & manage opportunities (org dashboard)

```js
// Fetch own opportunities for dashboard table
const opportunities = await api('/opportunities/mine/')

// Post new opportunity
const newOpp = await api('/opportunities/', {
  method: 'POST',
  body: {
    title: 'UI/UX Internship',
    organization_name: 'TechCo SA',
    description: 'Join our design team...',
    opportunity_type: 'Internship',
    category: 'Design',
    location: 'Riyadh, Saudi Arabia',
    external_url: 'https://techcosa.com/apply',
    application_deadline: '2026-08-01',
    is_paid: true,
    is_urgent: false,
  }
})

// Edit (partial)
await api('/opportunities/12/', {
  method: 'PATCH',
  body: { location: 'Hybrid', is_urgent: true }
})

// Delete
await api('/opportunities/12/', { method: 'DELETE' })
```

---

### Bookmarks & deadline tracker

```js
// Save a bookmark
const bookmark = await api('/bookmarks/', {
  method: 'POST',
  body: { opportunity_id: 12 }
})

// List bookmarks (sorted by nearest deadline — use as-is for Deadline Tracker)
const { results } = await api('/bookmarks/')

// Remove a bookmark — use the bookmark's own id, not the opportunity id
await api(`/bookmarks/${bookmark.id}/`, { method: 'DELETE' })

// Deadline tracker display logic
results.forEach(({ id, opportunity }) => {
  const deadline = new Date(opportunity.application_deadline)
  const today = new Date()
  const daysLeft = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24))

  if (daysLeft < 0) {
    // "Expired" — red bar
  } else {
    // `${daysLeft} days left` — green/yellow bar
  }
})
```

---

### Error handling pattern

```js
try {
  const data = await api('/opportunities/', { method: 'POST', body: payload })
  // success
} catch (err) {
  // err is the parsed JSON error body from the API
  if (err.detail) {
    showToast(err.detail)                          // e.g. "Authentication credentials were not provided."
  } else {
    // field-level validation errors
    Object.entries(err).forEach(([field, messages]) => {
      setFieldError(field, messages[0])            // e.g. { organization_name: ["This field is required."] }
    })
  }
}
```

---

### Session restore on page load

```js
async function restoreSession() {
  const token = localStorage.getItem('ohToken')
  if (!token) return null

  try {
    const user = await api('/auth/me/')
    return user
  } catch {
    // Token expired or invalid — clean up
    localStorage.removeItem('ohToken')
    localStorage.removeItem('ohUser')
    return null
  }
}
```

---

## Quick Reference

```
PUBLIC (no token needed)
  GET  /opportunities/             Browse all
  GET  /opportunities/{id}/        Single opportunity
  GET  /profiles/{username}/       Public profile

PROTECTED (token required)
  POST   /auth/logout/
  GET    /auth/me/
  GET    /profiles/me/
  PATCH  /profiles/me/
  DELETE /profiles/me/
  POST   /opportunities/           Create
  PATCH  /opportunities/{id}/      Edit (owner only)
  DELETE /opportunities/{id}/      Delete (owner only)
  GET    /opportunities/mine/      My posted opportunities
  GET    /bookmarks/               Student only
  POST   /bookmarks/               Student only
  DELETE /bookmarks/{id}/          Student only
```