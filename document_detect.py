import cv2
import numpy as np

def order_points(points):
    points = points.reshape(4, 2)

    rect = np.zeros((4, 2), dtype="float32")

    s = points.sum(axis=1)
    rect[0] = points[np.argmin(s)]
    rect[2] = points[np.argmax(s)]

    diff = np.diff(points, axis=1)
    rect[1] = points[np.argmin(diff)]
    rect[3] = points[np.argmax(diff)]

    return rect

def four_point_transform(image, points):
    rect = order_points(points)

    (tl, tr, br, bl) = rect

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))

    destination = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    matrix = cv2.getPerspectiveTransform(rect, destination)

    warped = cv2.warpPerspective(
        image,
        matrix,
        (maxWidth, maxHeight)
    )

    return warped

camera = cv2.VideoCapture(0)

camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

while True:
    success, frame = camera.read()

    if not success:
        break

    image = frame.copy()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(
        blur,
        50,
        150
    )

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    document = None

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < 5000:
            continue

        perimeter = cv2.arcLength(contour, True)
        corners = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        if len(corners) == 4:
            document = corners
            break

    if document is not None:
        cv2.drawContours(image, [document], -1, (0, 255, 0), 3)

    cv2.imshow("Paper Detection", image)
    cv2.imshow("Original", frame)
    cv2.imshow("Gray", gray)
    cv2.imshow("Blur", blur)
    cv2.imshow("Edges", edges)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("s"):

        if document is not None:

            scanned = four_point_transform(frame, document)

            scanned = cv2.resize(
                scanned,
                None,
                fx=2,
                fy=2,
                interpolation=cv2.INTER_CUBIC
            )

            scanned = cv2.fastNlMeansDenoisingColored(
                scanned,
                None,
                10,
                10,
                7,
                21
            )

            
            # Convert to grayscale
            gray_scan = cv2.cvtColor(scanned, cv2.COLOR_BGR2GRAY)

            # Improve local contrast (better than equalizeHist)
            clahe = cv2.createCLAHE(
                clipLimit=2.5,
                tileGridSize=(8, 8)
            )

            gray_scan = clahe.apply(gray_scan)

            # Remove camera noise while preserving text
            gray_scan = cv2.bilateralFilter(
                gray_scan,
                9,
                75,
                75
            )

            # Sharpen the document
            kernel = np.array([
                [-1, -1, -1],
                [-1,  9, -1],
                [-1, -1, -1]
            ])

            gray_scan = cv2.filter2D(
                gray_scan,
                -1,
                kernel
            )

            # Adaptive threshold (works better on documents)
            scanned = cv2.adaptiveThreshold(
                gray_scan,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                31,
                15
            )
            
            cv2.imshow("Scanned Document", scanned)

            cv2.imwrite(
                "scanned_document.jpg",
                scanned,
                [cv2.IMWRITE_JPEG_QUALITY, 100]
            )

            print("Document saved as scanned_document.jpg")

    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()