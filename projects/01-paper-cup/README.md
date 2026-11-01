# #01 Paper Cup

Fold a real drinking cup from one square of paper. Ages **6+**, about **10 minutes**.

**Coding / maths link:** the folds are an **algorithm** — a list of steps in order. Skip one and the cup fails (that is a bug!).

![Finished paper cup](final.png)

## You need
- 1 square of paper **150 × 150 mm** (origami paper, or cut a square from A4)
- A flat table and clean hands
- Optional: a sip of water to test the cup (grown-up nearby)

## Print the sheet
Download **[templates.pdf](templates.pdf)** (2× A4 pages). Print at **100% / Actual size** — do **not** choose “fit to page”. Measure the **100 mm** bar on the page with a ruler. If it is not exactly 100 mm, print again.

- [page-1.png](page-1.png) · [page-1.svg](page-1.svg) — cover, true-size square, symbol key, Finished! preview  
- [page-2.png](page-2.png) · [page-2.svg](page-2.svg) — steps 1–7 + Finished! check  
- [final.png](final.png) — vector finished cup  
- Machine-readable steps: [spec.json](spec.json)

## Symbol key
| Mark | Meaning |
|------|---------|
| Dashed **blue** | Valley fold (fold toward you) |
| Dash-dot **red** | Mountain fold (fold away) |
| ↻ | Turn the model over |
| → | Fold direction arrow |

## Step by step

1. **Diagonal valley** — Fold the top-left corner down to the bottom-right. Crease firmly. CHECK ✓: a triangle.
2. **Left corner up** — Fold the left tip up to the top peak. CHECK ✓: left flap meets the peak.
3. **Right corner up** — Fold the right tip up the same way (symmetry!). CHECK ✓: both sides match.
4. **Front lip down** — Fold the front top peak down into the little pocket. CHECK ✓: front lip tucked.
5. **Turn over** — Flip the whole model like a pancake.
6. **Back lip down** — Tuck the back peak the same way as step 4. CHECK ✓: both lips locked.
7. **Open the cup** — Squeeze the sides gently and push the bottom flat. CHECK ✓: a 3D cup with two flaps tucked!

## Finished!
Your cup should look like [final.png](final.png): open top, tapered body, **two flaps folded down** (front and back), flat bottom.

## Try it
Fold a second cup from a magazine page. Same algorithm — does it still work?

## Generator
Sheets are built by [`tools/paper_cup.py`](../../tools/paper_cup.py) (run from that folder’s parent with `python3 tools/paper_cup.py`).

## Video
Episode for the **Origami for Kids** playlist on [@Kids.JoinDev](https://www.youtube.com/@Kids.JoinDev) — coming soon.
