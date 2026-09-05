def merge_sort(movies):

    # Base case
    if len(movies) <= 1:
        return movies

    # Find middle
    middle = len(movies) // 2

    # Divide the list
    left = merge_sort(movies[:middle])
    right = merge_sort(movies[middle:])

    # Merge sorted parts
    return merge(left, right)


def merge(left, right):

    result = []

    i = 0
    j = 0

    # Compare elements from both lists
    while i < len(left) and j < len(right):

        # Sort by recommendation score
        if left[i][1] >= right[j][1]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Add remaining elements
    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result
