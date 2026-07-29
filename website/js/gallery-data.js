/* ============================================================
   Reclaim Era — Gallery & Events data
   ------------------------------------------------------------
   Featured photographs sourced from the client-managed Reclaim Era gallery.
   Add or reorder entries below whenever new event photographs are approved.

   Fields:
     id          any unique number
     imageUrl    full https link to the photo (or leave "" to show a
                 "Photo coming soon" placeholder tile)
     title       event name / short heading
     description one or two lines about the event
     date        any readable text, e.g. "March 2026" or "12 Mar 2026"

   Copy a block, change the values, done. Order here = order on the page.
   ============================================================ */
window.RE_GALLERY = [
  {
    id: 1,
    imageUrl: "assets/gallery/gallery-08.jpg",
    title: "Environmental education in action",
    description: "Volunteers and children coming together for a hands-on community learning activity.",
    date: "From the field"
  },
  {
    id: 2,
    imageUrl: "assets/gallery/gallery-02.jpg",
    title: "Blanket distribution",
    description: "Warm blankets reaching community members through Reclaim Era's donation programme.",
    date: "Community outreach"
  },
  {
    id: 3,
    imageUrl: "assets/gallery/gallery-04.jpg",
    title: "Toys finding a second home",
    description: "Pre-loved toys and play materials shared with children instead of being discarded.",
    date: "Reuse in action"
  },
  {
    id: 4,
    imageUrl: "assets/gallery/gallery-05.jpg",
    title: "Furniture donation",
    description: "Useful household furniture reclaimed and passed on to a family that can use it.",
    date: "Household reuse"
  },
  {
    id: 5,
    imageUrl: "assets/gallery/gallery-03.jpg",
    title: "Community donation drive",
    description: "A joyful moment with children during one of Reclaim Era's neighbourhood outreach activities.",
    date: "Community impact"
  }
  // , { id: 6, imageUrl: "https://...", title: "...", description: "...", date: "..." }
];
