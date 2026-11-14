"""
Academic content of the project.

The website (app.py) and the Word report are both built from this file, so the
text, equations, tables and pseudocode are the same in both.

The project is about the Isolation Forest algorithm. The five main sections
follow the course requirements and our four original files (explanation,
pseudocode, time complexity, and the original paper by Liu, Ting and Zhou, 2008).
The network traffic example is only an extra section at the end of the website.

Block types:
    ("p", text)                       paragraph, **bold** allowed
    ("h", text)                       sub-heading
    ("bullets", [text, ...])
    ("steps", [(title, text), ...])   numbered steps
    ("table", headers, rows)
    ("eq", latex, plain_text)         display equation
    ("code", title, text)             pseudocode block
    ("img", file_name, caption)       figure from assets/
    ("note", text)                    highlighted key idea
"""

SECTIONS = [
    # ------------------------------------------------------------------ 1
    {
        "id": "introduction",
        "title": "Introduction",
        "blocks": [
            ("h", "What Is Isolation Forest?"),
            ("p", "**Isolation Forest (iForest)** is an algorithm for anomaly detection. It was introduced by Liu, Ting, "
                  "and Zhou in 2008. It finds unusual points in a dataset in a simple and fast way, by checking how "
                  "easily each point can be separated (isolated) from the others using random splits."),
            ("p", "**Anomaly detection** means finding the observations that do not behave like the rest of the data. "
                  "These observations are called anomalies (or outliers). For example, a transaction that is much "
                  "larger than all the others, or a sensor reading that suddenly jumps far above its normal range."),
            ("p", "Isolation Forest is **unsupervised**, which means it does not need labeled data. We do not tell it "
                  "which points are normal and which are anomalies. It only uses the values of the data itself. The "
                  "purpose of the algorithm is to give every point an **anomaly score**, so the points can be ranked "
                  "from the most unusual to the most normal."),
            ("h", "The Main Idea"),
            ("p", "Most anomaly detection methods first learn what \"normal\" looks like, then mark anything far from "
                  "normal as an anomaly. Isolation Forest does the opposite. Anomalies are **few and different**, so "
                  "they are easy to separate from the rest of the data using only a few random splits. Normal points "
                  "sit inside dense groups of similar points, so they need many more splits."),
            ("h", "A Simple Example"),
            ("p", "Imagine a class of 30 students. We want to find one student by asking as few questions as possible. "
                  "A normal student looks like everyone else, so we need many questions. But a student wearing an "
                  "astronaut suit can be found with one question: \"Are you wearing a space suit?\" The student who is "
                  "found fast is the odd one."),
            ("note", "**Key idea:** A point that is isolated quickly (short path) is an anomaly. A point that takes "
                     "many splits to isolate (long path) is normal."),
            ("p", "This is a general tendency, not a rule for every point. An anomaly that is close to normal points, "
                  "or that belongs to a large group of similar anomalies, can need more splits. This is why the "
                  "algorithm averages the result over many trees."),
            ("img", "fig_isolation.png",
             "Figure 1. Isolating a normal point (left) and an anomaly (right) with random splits. Each split uses a "
             "random feature and a random value between its minimum and maximum. Averaged over 300 runs, the normal "
             "point needed 10.8 splits and the anomaly needed 2.6."),
        ],
    },
    # ------------------------------------------------------------------ 2
    {
        "id": "how-it-works",
        "title": "How It Works",
        "blocks": [
            ("p", "Isolation Forest works in two stages. In the **training stage** it builds a forest of isolation "
                  "trees from small random samples. In the **evaluation stage** it passes every point through the "
                  "trees, measures its path lengths and turns them into an anomaly score."),
            ("steps", [
                ("Build many random trees",
                 "The algorithm builds a forest of trees (called iTrees). Each tree uses a small random sample of the "
                 "data (ψ points, usually 256), not all of it. The sample is taken without replacement."),
                ("Split randomly",
                 "At each node, pick a random feature, then pick a random split value between the smallest and largest "
                 "value of that feature. Data goes left (value < split) or right (value ≥ split)."),
                ("Repeat",
                 "Keep splitting until every point is alone, all remaining points have the same values, or the tree "
                 "reaches a maximum depth. The depth limit is l = ⌈log₂ ψ⌉ (8 for ψ = 256), because anomalies are "
                 "isolated early and we do not need to fully isolate normal points."),
                ("Measure the path length",
                 "The path length h(x) is the number of splits (edges) a point passes through from the root until it "
                 "reaches a leaf. If the leaf still has more than one point because of the depth limit, an adjustment "
                 "c(size) is added to estimate the splits that were not built."),
                ("Take the average",
                 "Average the path length of each point over all trees. This reduces the effect of randomness."),
                ("Calculate the anomaly score",
                 "Convert the average path length into a score between 0 and 1 (see Anomaly Score below)."),
                ("Identify the anomalies",
                 "Sort the points by score. Points with the highest scores are reported as anomalies, either the top m "
                 "points or all points above a threshold."),
            ]),
            ("h", "Isolation Tree and Isolation Forest"),
            ("p", "One tree is called an **Isolation Tree (iTree)**. It is a binary tree: every internal node has one "
                  "test (feature < split value) and exactly two children, and every leaf is an external node. Because "
                  "its splits are random, one tree alone is not reliable. The **Isolation Forest** is the group of all "
                  "t iTrees, and its result for a point is the average over all of them. Isolation Forest is not the "
                  "same as Random Forest: Random Forest is a supervised classifier that chooses the best split using "
                  "labels, while Isolation Forest uses completely random splits and needs no labels."),
            ("h", "Small Example"),
            ("p", "We have five values of one numerical feature, for example five transaction amounts:"),
            ("table", ["Point", "Value", "Status"], [
                ["Point 1", "90", "Normal"],
                ["Point 2", "100", "Normal"],
                ["Point 3", "110", "Normal"],
                ["Point 4", "120", "Normal"],
                ["Point 5", "50,000", "Unusual"],
            ]),
            ("p", "If the random split value is between 120 and 50,000 (for example 21,000), Point 5 is separated alone "
                  "in the very first split (path length = 1). Since the split value is chosen between 90 and 50,000, "
                  "this happens in more than 99% of cases. The other four stay together and need more splits. After "
                  "repeating this on hundreds of trees, Point 5 still has a very short average path, so its anomaly "
                  "score is high."),
            ("img", "fig_itree_example.png", "Figure 2. One possible iTree for the five values."),
            ("h", "Anomaly Score"),
            ("p", "The anomaly score of a point x, when each tree is built from a sample of size ψ, is:"),
            ("eq", r"s(x, \psi) = 2^{\displaystyle -\frac{E[h(x)]}{c(\psi)}}", "s(x, ψ) = 2^( −E[h(x)] / c(ψ) )"),
            ("p", "**E[h(x)]** is the average path length of the point over all trees. **c(ψ)** is the average path "
                  "length we expect for a sample of size ψ. It is used to normalize the score so results can be "
                  "compared. It comes from the average path length of an unsuccessful search in a Binary Search Tree:"),
            ("eq", r"c(n) = 2H(n-1) - \frac{2(n-1)}{n}, \qquad H(i) \approx \ln(i) + 0.5772156649",
             "c(n) = 2H(n − 1) − 2(n − 1)/n,    H(i) ≈ ln(i) + 0.5772156649"),
            ("p", "H(i) is the harmonic number and 0.5772156649 is Euler's constant. For ψ = 256, c(256) ≈ 10.24. "
                  "(The paper writes the score as s(x, n), where n is the sample size used to build the trees, which "
                  "is ψ in iForest.)"),
            ("table", ["Score", "Average path", "Meaning"], [
                ["Close to 1", "Very short", "Anomaly (isolated quickly)"],
                ["Much smaller than 0.5", "Long", "Normal"],
                ["Around 0.5 for all points", "Near average", "No clear anomaly in the data"],
            ]),
            ("p", "**Example:** with ψ = 256, a point with an average path of 3 gets s = 2^(−3/10.24) ≈ 0.82, so it is "
                  "suspicious. A point with an average path of 14 gets s ≈ 0.39, so it looks normal."),
            ("h", "Main Parameters"),
            ("table", ["Parameter", "Meaning", "Common value"], [
                ["**n_estimators** (t)", "Number of trees in the forest. More trees give more stable results.", "100"],
                ["**max_samples** (ψ)", "Number of data points used to build each tree.", "256"],
                ["**contamination**", "Expected share of anomalies in the data. It sets the threshold between normal "
                                      "and anomaly.", "Depends on data (e.g. 0.01)"],
            ]),
            ("p", "The paper has only two parameters, t and ψ. The contamination parameter comes from the scikit-learn "
                  "implementation. If it is set to 'auto', scikit-learn uses the paper's 0.5 score as the threshold."),
        ],
    },
    # ------------------------------------------------------------------ 3
    {
        "id": "applications",
        "title": "Applications",
        "blocks": [
            ("p", "Isolation Forest is a general-purpose anomaly detection algorithm. It can be used in any field where "
                  "we have many numerical records, few or no labels, and a need to find the few unusual ones:"),
            ("table", ["Field", "What looks unusual", "Example features"], [
                ["Fraud detection", "Payments that do not match a customer's usual behavior", "Amount, location, time of day"],
                ["Financial transactions", "Unusual transfers or trading activity", "Transfer size, frequency, account age"],
                ["Industrial equipment monitoring", "Machines drifting away from normal operation, early faults",
                 "Vibration, temperature, pressure"],
                ["Sensor data", "Faulty, stuck or broken readings", "Reading value, rate of change"],
                ["System monitoring", "Servers or services behaving differently from usual", "CPU and memory use, response time"],
                ["Unusual user behavior", "Strange activity on an account, such as logins at odd times", "Login hour, failed attempts"],
                ["Network traffic", "Connections with unusual size or rate", "Packets per second, bytes sent, duration"],
            ]),
            ("p", "In every case, Isolation Forest only says that a record is unusual. It does not explain the cause, "
                  "so a flagged record still needs to be checked by a person or another system."),
            ("h", "Advantages and Disadvantages"),
            ("table", ["Advantages", "Disadvantages"], [
                ["Fast. Time grows almost linearly with data size.",
                 "Sensitive to the contamination (threshold) value."],
                ["Uses little memory because it uses small samples.",
                 "Less accurate when there are many useless (irrelevant) features. Results depend on choosing good features."],
                ["Unsupervised. No labeled data needed.", "Hard to explain why a specific point is an anomaly."],
                ["Works well with large datasets.",
                 "Can give false alarms (false positives) if normal behavior is very varied."],
                ["Does not calculate distances between points.",
                 "Results can change a little between runs because of randomness (a fixed random seed fixes this)."],
            ]),
        ],
    },
    # ------------------------------------------------------------------ 4
    {
        "id": "pseudocode",
        "title": "Pseudocode",
        "blocks": [
            ("p", "The pseudocode follows the three algorithms in the original paper. Algorithm 1 builds the forest, "
                  "Algorithm 2 builds one tree, and Algorithm 3 finds the path length of a point, which is then used "
                  "to compute the anomaly score."),
            ("h", "Algorithm 1: iForest(X, t, ψ)"),
            ("code", "",
             "// Problem Description: Build an ensemble (forest) of isolation trees (iTrees)\n"
             "// from the input data, to be used later for detecting\n"
             "// anomalies (points that are isolated with few splits).\n"
             "// Input:  X - input data set of n instances\n"
             "//         t - number of trees to build\n"
             "//         ψ - sub-sampling size (number of instances used per tree)\n"
             "// Output: Forest - a set of t iTrees\n"
             "{\n"
             "1. Forest ← { }                  // Initialize Forest as an empty set\n"
             "2. l ← ceiling(log2(ψ))          // Set the tree height limit\n"
             "3. for i ← 1 to t do\n"
             "   {\n"
             "4.     X' ← sample(X, ψ)         // Randomly select ψ instances from X\n"
             "5.     Tree ← iTree(X', 0, l)    // Build one iTree, starting at depth 0\n"
             "6.     Forest ← Forest ∪ {Tree}  // Add the new tree to the forest\n"
             "   }\n"
             "   endfor\n"
             "7. return Forest\n"
             "}"),
            ("h", "Inputs and Output"),
            ("bullets", [
                "**X**: the full input dataset.",
                "**t**: the number of trees to build. The paper's default is 100.",
                "**ψ**: the sub-sampling size, meaning how many data points each tree is built from. The default is 256.",
                "**Output**: a forest of t isolation trees (iTrees).",
            ]),
            ("h", "Step-by-Step Explanation"),
            ("steps", [
                ("Initialize Forest",
                 "Start with an empty forest that has no trees yet. The next steps fill it."),
                ("Set height limit l = ceiling(log2 ψ)",
                 "Set the maximum depth any tree may reach. log2 ψ is roughly the average depth of a binary tree built "
                 "from ψ points, and ceiling rounds the value up. Example: if ψ = 256, then l = log2(256) = 8. Why limit "
                 "the height? Anomalies are isolated quickly, with only a few splits, so they end up close to the root. "
                 "Normal points sit deeper in the tree, and there is no need to keep splitting until every one of them "
                 "is isolated. Stopping early saves time and memory."),
                ("for i = 1 to t do",
                 "A loop that runs t times. Each pass builds one tree."),
                ("X' ← sample(X, ψ)",
                 "Randomly draw a small sub-sample of size ψ from the full dataset, without replacement. Each tree is "
                 "built from this small subset, not from all the data. This is one of the paper's key ideas, because "
                 "small sub-samples reduce two problems: **swamping**, where normal points get wrongly flagged as "
                 "anomalies because they are close to anomalies, and **masking**, where anomalies hide because there "
                 "are many of them grouped together."),
                ("Tree ← iTree(X', 0, l)",
                 "Build an isolation tree from the sub-sample X'. 0 is the current depth, so building starts at the "
                 "root, and l is the height limit from Step 2. Algorithm 2 describes how the tree is built."),
                ("Forest ← Forest ∪ {Tree}",
                 "Add the new tree to the forest. The loop ends once all t trees have been built."),
                ("return Forest",
                 "Return the complete forest."),
            ]),
            ("img", "fig_workflow.png", "Figure 3. Workflow of Algorithm 1 (training the forest)."),
            ("h", "Algorithm 2: iTree(X, e, l)"),
            ("code", "",
             "// Problem Description: Build one isolation tree by recursive random partitioning.\n"
             "// Input:  X - input data (instances that reached this node)\n"
             "//         e - current tree height (depth)\n"
             "//         l - height limit\n"
             "// Output: an iTree\n"
             "{\n"
             "1.  if e ≥ l or |X| ≤ 1 then         // limit reached or point isolated\n"
             "2.      return exNode{Size ← |X|}    // leaf stores its number of instances\n"
             "3.  else\n"
             "4.      let Q be a list of attributes in X\n"
             "5.      randomly select an attribute q ∈ Q\n"
             "6.      randomly select a split point p from max and min\n"
             "        values of attribute q in X\n"
             "7.      Xl ← filter(X, q < p)        // instances that go left\n"
             "8.      Xr ← filter(X, q ≥ p)        // instances that go right\n"
             "9.      return inNode{Left ← iTree(Xl, e + 1, l),\n"
             "10.                   Right ← iTree(Xr, e + 1, l),\n"
             "11.                   SplitAtt ← q,\n"
             "12.                   SplitValue ← p}\n"
             "13. end if\n"
             "}"),
            ("steps", [
                ("Stopping conditions (lines 1 and 2)",
                 "Stop when the depth e reaches the limit l, or when the node has 0 or 1 instance. The leaf (external "
                 "node) stores Size, the number of instances that reached it. The paper's definition also stops when "
                 "all instances in X have the same values, because no split is possible."),
                ("Random attribute (lines 4 and 5)",
                 "Pick one attribute q at random from the list of attributes."),
                ("Random split point (line 6)",
                 "Pick a split value p at random between the minimum and maximum of q in X."),
                ("Partition (lines 7 and 8)",
                 "Instances with q < p go to the left branch, the rest go to the right branch."),
                ("Recursion (lines 9 to 12)",
                 "Build the two children with depth e + 1, then return an internal node that stores the two children, "
                 "the split attribute and the split value."),
            ]),
            ("h", "Algorithm 3: PathLength(x, T, e)"),
            ("code", "",
             "// Problem Description: Find the path length of instance x in one iTree.\n"
             "// Input:  x - an instance\n"
             "//         T - an iTree\n"
             "//         e - current path length; 0 on the first call\n"
             "// Output: path length of x\n"
             "{\n"
             "1. if T is an external node then\n"
             "2.     return e + c(T.size)      // c(.) from the anomaly score section\n"
             "3. end if\n"
             "4. a ← T.splitAtt\n"
             "5. if x_a < T.splitValue then\n"
             "6.     return PathLength(x, T.left, e + 1)\n"
             "7. else                          // x_a ≥ T.splitValue\n"
             "8.     return PathLength(x, T.right, e + 1)\n"
             "9. end if\n"
             "}"),
            ("steps", [
                ("Reaching a leaf (lines 1 and 2)",
                 "When x reaches an external node, return the number of edges counted so far (e) plus c(T.size). If "
                 "the leaf has one instance, c(1) = 0. If it has more (because the tree stopped at the height limit), "
                 "c(T.size) estimates how much deeper the path would have gone."),
                ("Moving down the tree (lines 4 to 8)",
                 "Compare x on the node's split attribute with the split value, move to the left or right child, and "
                 "add one edge."),
                ("Computing the anomaly score",
                 "Run PathLength(x, T, 0) for every tree in the forest, take the average to get E[h(x)], and compute "
                 "s(x, ψ) = 2^(−E[h(x)] / c(ψ)). To find the top m anomalies, sort all points by s from highest to "
                 "lowest and take the first m."),
            ]),
        ],
    },
    # ------------------------------------------------------------------ 5
    {
        "id": "time-complexity",
        "title": "Time Complexity",
        "blocks": [
            ("h", "1. Overview and Basic Parameters"),
            ("p", "Isolation Forest takes a small random sample of the data and recursively partitions it into binary "
                  "trees (iTrees) up to a maximum depth. Because every tree is built from a fixed-size sample and has a "
                  "limited height, the cost of building the forest does not depend on the dataset size, and the cost "
                  "of evaluating the data grows linearly with it. This gives the algorithm a linear time complexity "
                  "**O(n)** when t and ψ are fixed."),
            ("p", "The time complexity depends on four main variables:"),
            ("table", ["Symbol", "Meaning", "Default value"], [
                ["**n**", "Total number of data points (instances) to analyze", "Variable (e.g. 10,000 to 1,000,000+)"],
                ["**t**", "Number of trees in the forest", "100 trees"],
                ["**ψ**", "Sub-sample size used to build one tree", "256 data points"],
                ["**l**", "Maximum tree depth: l = ⌈log₂ ψ⌉", "8 levels (since log₂ 256 = 8)"],
            ]),
            ("p", "**Assumptions:** the data is already loaded in memory, so any point can be read in O(1); choosing a "
                  "random feature, choosing a random split value, and comparing two values each take O(1); and every "
                  "tree uses the height limit l, as in the paper."),
            ("h", "2. Training Time Complexity (Building the Forest)"),
            ("p", "In the training phase, the algorithm builds t trees using random sub-samples of size ψ:"),
            ("bullets", [
                "**Step 1 (Sampling):** picking ψ random data points from the dataset takes O(ψ).",
                "**Step 2 (Building 1 tree):** at each level, the ψ data points are split into left and right branches "
                "in O(ψ) time (finding the min and max of the chosen feature and splitting the points). Since the tree "
                "has at most ⌈log₂ ψ⌉ levels, building one tree takes O(ψ · log₂ ψ).",
                "**Step 3 (Building t trees):** repeating this for t trees gives the total training time:",
            ]),
            ("eq", r"T_{\text{train}} = O(t \cdot \psi \log_2 \psi)", "Training time complexity: O(t · ψ log₂ ψ)"),
            ("p", "Because t (100) and ψ (256) are fixed, building the forest does **not** increase when the dataset "
                  "size n grows, so it is constant with respect to n. This does not mean the whole process is O(1): "
                  "the data still has to be read (O(n · d) for d features), and every point still has to be evaluated "
                  "in the testing phase."),
            ("h", "3. Testing Time Complexity (Evaluating Data Points)"),
            ("p", "In the testing (evaluation) phase, we pass all n data points through the forest to find their path "
                  "length (depth):"),
            ("bullets", [
                "**Step 1 (1 data point in 1 tree):** a data point starts at the root and moves down at most ⌈log₂ ψ⌉ "
                "levels, taking O(log₂ ψ) comparisons. Adding c(size) at the leaf takes O(1).",
                "**Step 2 (1 data point in t trees):** testing one data point across all t trees takes O(t · log₂ ψ).",
                "**Step 3 (All n data points):** testing all n data points across the forest gives:",
            ]),
            ("eq", r"T_{\text{test}} = O(n \cdot t \log_2 \psi) \approx O(n)", "Testing time complexity: O(n · t log₂ ψ) ≈ O(n)"),
            ("p", "Since t and ψ are small fixed numbers, the testing time grows linearly, O(n), with the number of data "
                  "points. Comparing the scores with a threshold adds O(n). If all points are sorted to rank them, "
                  "sorting adds O(n log n)."),
            ("table", ["Phase", "Formula", "Simplified Big-O", "Why?"], [
                ["**Reading / sampling data**", "O(n · d) to load, O(t · ψ) to sample", "O(n)",
                 "The data must be read once; each tree samples ψ points"],
                ["**Training phase**", "O(t · ψ log₂ ψ)", "Constant with respect to n",
                 "Uses fixed sample size (ψ = 256) and fixed trees (t = 100)"],
                ["**Testing phase**", "O(n · t log₂ ψ)", "O(n), linear",
                 "Evaluates each of the n data points through t trees of depth log₂ ψ"],
                ["**Total time**", "O(t · (ψ + n) log₂ ψ)", "O(n), linear",
                 "Dominated by evaluating n data points when n is large"],
            ]),
            ("h", "4. Best, Average, and Worst-Case Time Complexity"),
            ("bullets", [
                "**Best case: O(t) per data point (anomalous points).** Anomalies have extreme values, so they are "
                "often isolated at the top of the tree (depth 1 or 2) without reaching the bottom. This takes O(1) per "
                "tree, or O(t) across all trees, and O(n · t) if every point were like this.",
                "**Average case: O(n · t log₂ ψ) (normal data points).** Normal data points need more splits and travel "
                "down to about the average tree depth log₂ ψ, giving O(n · t log₂ ψ) ≈ O(n). Training in the average "
                "case is O(t · ψ log₂ ψ).",
                "**Worst case: O(n · t log₂ ψ) (protected by the height limit).** Without a height limit, a badly "
                "unbalanced tree could grow to depth ψ − 1. Training would slow down to O(t · ψ²) and testing to "
                "O(n · t · ψ). Because the algorithm stops every tree at height l = ⌈log₂ ψ⌉, the worst case never "
                "exceeds O(t · ψ log₂ ψ) for training and O(n · t log₂ ψ) for testing.",
            ]),
            ("table", ["Case", "Single data point", "Full dataset (n)", "Simple explanation"], [
                ["**Best case**", "O(t)", "O(n · t)", "Anomalous points are isolated near the root (depth 1–2)"],
                ["**Average case**", "O(t · log₂ ψ)", "O(n · t log₂ ψ) ≈ O(n)", "Normal data points reach the average depth log₂ ψ"],
                ["**Worst case**", "O(t · log₂ ψ)", "O(n · t log₂ ψ) ≈ O(n)", "Tree height limit l = 8 prevents deeper trees"],
                ["**Worst case without height limit**", "O(t · ψ)", "O(n · t · ψ)", "A fully grown, unbalanced tree can reach depth ψ − 1"],
            ]),
            ("h", "5. Space Complexity"),
            ("p", "Each tree has at most 2ψ − 1 nodes (511 nodes for ψ = 256), so the forest needs O(t · ψ) memory. "
                  "This does not depend on n, which is why Isolation Forest uses little memory."),
            ("h", "6. Note on the scikit-learn Implementation"),
            ("p", "scikit-learn follows the same limits as the paper: max_samples='auto' uses ψ = min(256, n), and the "
                  "maximum tree depth is ⌈log₂ ψ⌉. One difference: when contamination is a number, fit() also scores "
                  "all training points to choose the threshold, which adds O(n · t log₂ ψ) to the training step."),
            ("note", "**Summary for the presentation:** training builds t small trees, each from ψ points and at most "
                     "log₂ ψ levels deep, so it costs O(t · ψ log₂ ψ) and does not depend on n. Testing sends each of "
                     "the n points down t trees, so it costs O(n · t log₂ ψ). With t and ψ fixed, the whole algorithm "
                     "grows linearly with n."),
        ],
    },
]

DEMO_TITLE = "Additional Practical Example: Network Traffic Anomaly Detection"

DEMO_INTRO = (
    "Isolation Forest can be applied in different fields. One example is network traffic anomaly detection, where "
    "unusual connections can be identified based on their numerical characteristics. To demonstrate this "
    "application, we developed a small interactive example using the CICIDS2017 dataset."
)

REFERENCES = [
    "Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2008). Isolation Forest. In Proceedings of the 8th IEEE International "
    "Conference on Data Mining (ICDM 2008) (pp. 413–422). IEEE. https://doi.org/10.1109/ICDM.2008.17",
    "Liu, F. T., Ting, K. M., & Zhou, Z.-H. (2012). Isolation-based anomaly detection. ACM Transactions on Knowledge "
    "Discovery from Data, 6(1), Article 3, 1–39. https://doi.org/10.1145/2133360.2133363",
    "Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., et al. (2011). Scikit-learn: "
    "Machine learning in Python. Journal of Machine Learning Research, 12, 2825–2830.",
    "scikit-learn developers. (n.d.). sklearn.ensemble.IsolationForest [API documentation]. Retrieved November 14, "
    "2026, from https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html",
    "Sharafaldin, I., Habibi Lashkari, A., & Ghorbani, A. A. (2018). Toward generating a new intrusion detection "
    "dataset and intrusion traffic characterization. In Proceedings of the 4th International Conference on "
    "Information Systems Security and Privacy (ICISSP 2018) (pp. 108–116). SciTePress. "
    "https://doi.org/10.5220/0006639801080116",
    "Canadian Institute for Cybersecurity. (n.d.). Intrusion detection evaluation dataset (CIC-IDS2017). University "
    "of New Brunswick. Retrieved November 14, 2026, from https://www.unb.ca/cic/datasets/ids-2017.html",
]
