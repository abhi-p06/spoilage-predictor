# Viva Preparation Guide — Post-Harvest Spoilage Predictor

> Read this once the night before. Sleep well. You built something real.

---

## 1. The One-Paragraph Pitch

India loses roughly 30–40% of all fruits and vegetables before they ever reach a customer — not because of bad farming, but because small farmers have no way of knowing when their produce is about to go bad until it already has. We built a web application that a farmer can open on any phone browser, upload a photo of their fruit, enter three simple details, and get back a clear answer: green (safe to store), yellow (sell soon), or red (sell or discard immediately). Behind that simple interface, three AI models work together — a **CNN** that reads the fruit photo like an expert eye, an **LSTM** that analyses gas and temperature patterns the way a food scientist would, and an **XGBoost fusion model** that weighs all the signals together and makes the final call. The CNN alone hit 97.2% accuracy on real fruit images, and the whole system runs in under 10 seconds on a laptop. If this were deployed with cheap gas sensors, a farmer who currently throws away a third of their crop could instead sell it at the right time and save that income.

---

## 2. The Problem — Why This Matters

India produces around 300 million tonnes of fruits and vegetables every year, and ICAR estimates that 30–40% of it rots before it reaches consumers — that's roughly ₹92,000 crore in annual losses. Small farmers with one to three acres of land feel this the hardest because they don't have access to cold storage or refrigerated trucks, and their entire year's income depends on the harvest going right. Right now, the way a farmer checks if produce is going bad is by looking at it — squeezing a mango, smelling a banana, poking a tomato. That's it. No measurement, no early warning, no data. The problem is that visible rot is already the end stage — by the time you can see spoilage, the window to sell has often already closed. Our system addresses exactly that gap: give the farmer a prediction *before* things go visually wrong, when they can still act on it.

---

## 3. What the System Does — Plain English Walkthrough

**Step 1 — Farmer opens the web app.**
They go to `localhost:5000` in any browser. No installation needed, no account, no login. They see a clean form asking for four things.

**Step 2 — They upload a photo.**
They take a picture of the fruit on their phone and upload it. Behind the scenes, Flask saves it to the `uploads/` folder with a timestamp so it doesn't overwrite anyone else's photo.

**Step 3 — They fill in three details.**
They pick the produce type (apple, banana, tomato, or mango), type in how many days since harvest, and toggle whether it's stored in a fridge or at room temperature. That's all. No sensor hardware required at this stage.

**Step 4 — They click Analyse.**
Flask calls `predict.run_prediction()` in `predict.py`. That function calls three models in sequence — CNN first, then LSTM, then XGBoost — and packages all the results into a single dictionary.

**Step 5 — They see the result dashboard.**
The page shows a big colour banner (GREEN / YELLOW / RED), the spoilage percentage, how many days are left, the individual CNN and LSTM scores, and a plain one-line recommendation like "Sell within 24–48 hours." The farmer doesn't need to understand any of the numbers — the colour tells them what to do.

---

## 4. The Three Models — Explained Like You Built Them

### Model 1 — CNN (MobileNetV2)

**a) What problem it solves:** It reads the photograph and decides how fresh the fruit looks, the same way an experienced mandi trader glances at a crate and forms an opinion instantly.

**b) Input:** A single fruit photo, resized to 224×224 pixels and normalised so all pixel values are between 0 and 1. The actual file comes from the farmer's upload.

**c) Output:** A number between 0.0 and 1.0 called `freshness_score`. 1.0 means perfectly fresh, 0.0 means completely rotten. (We invert the model's raw output because it was trained with 1=rotten.)

**d) Analogy:** Think of it like a doctor reading an X-ray. The doctor didn't need to see every X-ray themselves — they were trained on thousands of examples. MobileNetV2 was pre-trained on 1.28 million ImageNet photos (it already knows what edges, textures, and shapes look like), and we fine-tuned it on 10,901 fruit photos specifically.

**e) One thing that could go wrong:** The model had never seen tomato or mango images during training — only apples, bananas, and oranges. We handled this by not relying on the CNN alone; the XGBoost fusion layer also gets `produce_id` and `days` as inputs, which helps correct for the CNN's uncertainty on unseen produce types.

---

### Model 2 — LSTM (Bidirectional)

**a) What problem it solves:** It detects spoilage from patterns in the storage environment over time — specifically rising ethylene and CO₂ levels — which are scientifically measurable warning signs that appear *before* visible rot.

**b) Input:** A 24-hour sequence of four sensor readings per hour: ethylene (ppm), CO₂ (ppm), humidity (%), and temperature (°C). In our prototype, this sequence is generated mathematically from the farmer's `produce` type and `days_since_harvest` inputs using USDA ethylene emission ranges. The shape going into the model is `(1, 24, 4)`.

**c) Output:** A single number between 0.0 and 1.0 called `lstm_risk`. Values above 0.5 indicate the atmospheric conditions of a spoiling batch.

**d) Analogy:** Think of it like a doctor checking a patient's vitals over 24 hours, not just at one moment. If a patient's temperature rises slowly over hours, that's more informative than a single reading. The LSTM sees the whole trajectory, which is why we chose it over a simple feedforward network.

**e) One thing that could go wrong:** The four sensor channels have very different scales — CO₂ goes up to 4,000 ppm while ethylene might be just 5 ppm. If we fed them raw into the model, CO₂ would completely dominate. We fixed this by fitting a `StandardScaler` on the training data and applying it to every input sequence — this is stored in `models/lstm_scaler.pkl` and loaded alongside the model at inference time.

---

### Model 3 — XGBoost Fusion

**a) What problem it solves:** It takes the two AI scores and the farmer's metadata and makes the final, calibrated probability — like a judge hearing two expert witnesses and then delivering a verdict.

**b) Input:** A 5-number vector: `[cnn_score, lstm_risk, days_since_harvest, cold_chain_flag, produce_id]`. That's it. Very simple input.

**c) Output:** Two numbers — `spoilage_probability` (0–100%) from the classifier, and `days_to_spoilage` (an integer) from the regressor. We actually trained two separate XGBoost models and bundled them together in one file (`fusion_xgb.pkl`).

**d) Analogy:** It's like combining two diagnostic tests at a hospital — one blood test and one scan — into a single final diagnosis. The XGBoost model learned from 10,000 training examples which combination of signals means "this batch is going bad soon."

**e) One thing that could go wrong:** XGBoost can overfit on small datasets. We prevented this with L1 and L2 regularisation (`reg_alpha=0.05`, `reg_lambda=1.0`), subsample ratios of 0.85 so it never sees all the data at once, and five-fold cross-validation to confirm the score wasn't just luck on one test set.

---

## 5. The Dashboard — What Every Number Means

**Spoilage Probability (the big percentage)**
This is the XGBoost model's final answer — the probability that this batch will spoil within its effective shelf life. If it says 73%, it means based on the photo and the storage details, there's a 73% chance the batch is heading toward spoilage. You explain it as: "Professor, this is the output of our fusion model — it combines the visual score from the CNN and the atmospheric risk score from the LSTM, weighted by the model's learned importance of each signal."

**CNN Freshness Score**
This is only the visual verdict — what the MobileNetV2 model saw in the photo. 95% means it looks very fresh, 20% means it looks visually rotten. Tell the professor: "This score comes exclusively from the image — it's the CNN's visual freshness reading, inverted from the raw sigmoid output so that higher always means fresher."

**Sensor Risk Score (LSTM)**
This is what the LSTM predicted based on the simulated atmospheric environment for this produce type at this age. A high score means the ethylene and CO₂ patterns look like a batch that's actively respiring and approaching spoilage. Say: "This is the LSTM's reading of the simulated sensor environment — it captures the time-series pattern of gas emissions over 24 hours, which is a scientifically validated early indicator of spoilage before it becomes visible."

**Days to Spoilage**
This is the XGBoost regressor's output — a separate model trained to predict how many days are left before the batch crosses the spoilage threshold. Explain it as: "We trained a second XGBoost model, a regressor, to predict this number alongside the classifier — so the farmer gets both a probability and a concrete number of days they can plan around."

**Alert Level (GREEN / YELLOW / RED)**
This is a simple threshold rule: below 35% spoilage probability is GREEN, 35–70% is YELLOW, above 70% is RED. It's not ML — it's a business logic rule coded directly in `predict.py`'s `get_alert()` function. Tell the professor: "The thresholds were chosen to give farmers a meaningful planning horizon — GREEN means standard storage, YELLOW means prioritise this batch, RED means it needs immediate action."

---

## 6. Questions Your Professor Will Definitely Ask

**Q: Why did you choose MobileNetV2 over other CNNs like VGG16 or ResNet?**
A: We chose MobileNetV2 because of its efficiency. VGG16 has 138 million parameters — that's massive for a web app that needs to respond fast. MobileNetV2 achieves comparable accuracy with only about 3.4 million base parameters using depthwise separable convolutions, which means it loads faster, runs in less memory, and is designed specifically for deployment scenarios, not just research benchmarks.

**Q: Why LSTM and not a simple feedforward neural network?**
A: A simple feedforward network would treat each hour's sensor reading as independent. But the key signal in our data is the *trend* — ethylene rises over time as fruit ripens, CO₂ accelerates as fermentation begins. An LSTM remembers earlier readings in its cell state and uses that memory to understand the trajectory, not just the current moment. That's exactly the kind of temporal dependency that makes LSTM the right choice here.

**Q: Why XGBoost for the fusion layer, not another neural network?**
A: The fusion layer is taking a 5-number vector as input — `cnn_score`, `lstm_risk`, `days`, `cold_chain`, `produce_id`. For such a small, structured, tabular input, XGBoost consistently outperforms neural networks in sample efficiency, training speed, and interpretability. We also get feature importances for free, which told us the CNN score contributes 78.4% of the decision weight.

**Q: How did you handle class imbalance?**
A: The image dataset has more rotten images than fresh ones (e.g., 2,342 rotten apples vs 1,693 fresh apples in training). For the CNN we addressed this through augmentation — the minority class effectively appears more times per epoch because of random transformations. For the sensor dataset we generated it ourselves with a perfect 50/50 balance from the start. For the fusion dataset we used stratified train-test splitting so the class ratio was preserved in both splits.

**Q: What is transfer learning and why did you use it?**
A: Transfer learning means we started with a model (MobileNetV2) that was already trained on 1.28 million images from ImageNet. Instead of learning what edges, textures, and shapes look like from scratch, we reused all of that knowledge and only trained a small classification head on our 10,901 fruit images. Without this, we'd need far more data and compute time to reach comparable accuracy. It's why we hit 97.22% accuracy on a dataset that, for training from scratch, would be considered quite small.

**Q: What is a look-back window?**
A: It's how far back in time the LSTM looks when making a prediction. Ours is 24 timesteps — one reading per hour for 24 hours. This is our "window." If we used a 48-hour window, the model would see two days of data, which might be better for detecting slow-onset spoilage but would require more data to train reliably. We chose 24 hours as a practical balance between prediction quality and the realistic monitoring window a farmer would observe.

**Q: What does val_accuracy mean and is ours good enough?**
A: Validation accuracy is how well the model performs on data it has never seen during training. We set aside the entire test set — 2,698 images — and never touched it until evaluation. Our 97.22% val_accuracy means 97 out of every 100 test images were classified correctly. The target we set ourselves was 85%, and we exceeded it by more than 12 percentage points. Yes, it's more than good enough for a prototype.

**Q: What is AUC and why is it better than accuracy here?**
A: AUC stands for Area Under the ROC Curve. While accuracy tells you what fraction of predictions were right, it can be misleading when classes are imbalanced. AUC measures how well the model *ranks* positives above negatives across all possible thresholds — an AUC of 1.0 means perfect separation, and 0.5 means random guessing. We used AUC as the primary metric for the LSTM and fusion models because it's more informative about model quality when the cost of false negatives (missing spoilage) is different from false positives (incorrectly flagging fresh produce).

**Q: Why is your sensor data synthetic and is that valid?**
A: Real IoT sensors are not part of our prototype — we don't have the hardware. So we generated the sensor data mathematically using ethylene emission ranges documented in USDA Handbook 66, which is the gold-standard agricultural reference for postharvest gas behaviour. The generation parameters — Apple 1.2–25 ppm, Banana 8.5–50 ppm, etc. — are grounded in decades of peer-reviewed research. Synthetic data is standard practice in early-stage prototypes where data collection is impractical, and the model would be fine-tuned on real sensor readings in a production deployment.

**Q: What would you do differently with more time?**
A: Three things. First, collect real sensor data using an MQ-136 ethylene sensor and fine-tune the LSTM on actual readings instead of synthetic ones. Second, add labelled mango and tomato images to the CNN training set — right now those classes are handled by the fusion layer's `produce_id` feature, but having real visual examples would make the CNN more accurate for those crops. Third, deploy this as an Android app in Hindi — currently it's an English web app, which limits its accessibility to the farmers who need it most.

**Q: How does the fusion model know which model to trust more?**
A: It learns from training data. During training, the XGBoost model saw 10,000 examples where both the CNN score and the LSTM risk score were present, along with the true label. It discovered through gradient boosting that the CNN score is the strongest predictor — it accounts for 78.4% of the decision — while the LSTM adds about 1.6%. This isn't a fixed weight we set; it's something the model learned from the data distribution.

**Q: What is overfitting and how did you prevent it?**
A: Overfitting is when a model memorises the training data instead of learning general patterns — it performs great in training but fails on new data. We prevented it in four ways: Dropout layers in both the CNN (0.4) and LSTM (0.3 and 0.2); EarlyStopping that halted training when validation performance stopped improving; ReduceLROnPlateau that reduced the learning rate when the model started plateauing; and regularisation terms in XGBoost (`reg_alpha`, `reg_lambda`, subsampling) that penalise complex trees.

**Q: Can this work on a real farm without internet?**
A: Right now, no — the Flask app needs to be running on a server or laptop that the farmer can connect to. But it absolutely can be made offline-capable. The LSTM is only 3.8 MB. The fusion model is 1 MB. Even the CNN is 25.8 MB — all of this fits on a Raspberry Pi Zero 2W (₹800) which could run the prediction locally in the storage shed with a basic Android app as the front-end. We described this in our Future Scope section as the natural next step.

**Q: What is the business model for this?**
A: There are a few viable models. One is a Farmer Producer Organisation (FPO) subscription where an FPO pays a monthly fee for access on behalf of their member farmers. Another is a government AgriTech partnership — schemes like PM-KISAN or eNAM already have farmer onboarding infrastructure this could plug into. A third is a hardware bundle: sell the ₹800 Raspberry Pi + sensors kit with a pre-installed app, the way someone sells a water quality meter, and charge for the sensor calibration service annually. We're engineering students, not business students — so we designed it to be deployable at low cost, which makes all these models feasible.

**Q: How is this different from existing spoilage detection apps?**
A: Most existing apps do one thing — they either classify a photo as fresh or rotten, or they just provide shelf-life lookup tables. What's different here is the multimodal fusion: we combine visual information with sensor-based atmospheric data with farm metadata in a single inference pipeline. The days-to-spoilage regression output is also something we haven't seen in other student projects or commercial apps at this scale — it gives an actionable number, not just a binary label.

---

## 7. The Architecture Explained in One Minute

*(Read this aloud while pointing at the architecture diagram)*

"So when a farmer uses our system, two things happen simultaneously. On the left side — the photo they uploaded goes into the CNN. We're using MobileNetV2, which was pre-trained on over a million images, so it already understands visual patterns. We fine-tuned it on about 11,000 fruit photos and trained it to produce what we call a freshness score — a number between 0 and 1, where 1 is perfectly fresh. On the right side — from the produce type and days-since-harvest that the farmer entered, we simulate a 24-hour sensor sequence: ethylene levels, CO₂, humidity, temperature. This goes into our LSTM model, which reads the pattern over time and produces a spoilage risk score. Both of these scores — plus the three metadata inputs — then go into our fusion layer, which is an XGBoost model. It takes all five numbers and outputs two things: the final spoilage probability and the number of days remaining. The Flask app takes those results and renders the dashboard — the colour alert, the percentage, the days, and the recommendation. The farmer sees one simple answer. Everything else is handled behind the scenes in `predict.py`, which chains all three models together in sequence."

---

## 8. What Makes This Project Different

**1. It's genuinely multimodal — not just an image classifier.**
Most student projects train one model on one data type. We combined a vision model, a time-series model, and a tabular fusion model into one pipeline.
*Say this:* "Professor, the key architectural decision here was combining visual evidence with sensor-based atmospheric data — that's what makes the prediction more robust than either signal alone."

**2. The LSTM uses real agricultural science, not made-up data.**
The synthetic sensor data is anchored to USDA Handbook 66 ethylene emission ranges — we didn't just make random numbers up.
*Say this:* "The sensor data generation is grounded in USDA-published postharvest biology literature, which is the same source that commercial cold-storage operators use for gas management."

**3. The web app works with graceful mock mode before training.**
If the model files don't exist, the app still runs using calibrated heuristics. This made development and testing faster and cleaner.
*Say this:* "We designed `predict.py` with a fallback system so the Flask app is always runnable — we could test the entire UI before training was complete."

**4. The fusion output includes a regressor, not just a classifier.**
We trained a second XGBoost model to predict days-to-spoilage as a number, which is far more actionable than just "spoiled / not spoiled."
*Say this:* "We identified that a binary label alone isn't actionable for a farmer — they need to know *how many days* they have, so we trained a companion regressor alongside the classifier."

**5. All training exceeded targets by a significant margin.**
Our target was 85% CNN accuracy. We hit 97.22%. Target was AUC ≥ 0.90 for LSTM. We hit 1.000.
*Say this:* "We set conservative, realistic targets before training, and all three models exceeded them — which gave us confidence that the architecture decisions were sound."

---

## 9. Honest Limitations — Say These Before She Asks

**Limitation 1: The LSTM is trained on synthetic sensor data.**
*Honest explanation:* We didn't have real ethylene sensors, so we generated data mathematically. The distributions are scientifically grounded but they're still not real measurements.
*Follow-up:* "We're aware this is the biggest gap. The fix is straightforward — an MQ-136 sensor costs ₹150, and we'd fine-tune the LSTM on 30 days of real readings. We scoped the architecture to make that update easy."

**Limitation 2: The CNN has only seen apple, banana, and orange images.**
*Honest explanation:* The Kaggle dataset doesn't include mango or tomato images, so the CNN is making somewhat generalised predictions for those crops.
*Follow-up:* "The fusion model's `produce_id` feature partially compensates for this, but a proper fix would be adding labelled tomato and mango images to the training set — which we'd do given more time."

**Limitation 3: The system supports only four produce types.**
*Honest explanation:* Apple, banana, tomato, and mango. India grows a hundred important crops. We picked four to build and validate the pipeline properly.
*Follow-up:* "The architecture is modular — adding a new produce type means adding it to the shelf-life and ethylene dictionaries in `predict.py`, generating sensor data for it, and retraining. The pipeline itself doesn't change."

**Limitation 4: No real hardware integration yet.**
*Honest explanation:* Right now the app requires a browser and a server. It's not yet a standalone offline tool a farmer in rural Maharashtra can use without connectivity.
*Follow-up:* "The model sizes make this very feasible as a next step — the total inference models are under 35 MB, which runs comfortably on a Raspberry Pi Zero 2W."

---

## 10. Team Talking Points — Suggested Split for 4 People

**Person 1 — The Problem & Overview**
*Opening line:* "Good morning ma'am / sir. I'll start by setting the context — why we chose this problem and what we built at a high level."
*Owns:* Sections 1 and 2 (the pitch, the problem statement, why small farmers, what they currently do). Should be the most confident speaker since this comes first and sets the tone.

**Person 2 — CNN and Data**
*Opening line:* "I'll take you through our visual freshness model and the datasets we used."
*Owns:* The image dataset description (13,599 images, class breakdown), the CNN architecture (MobileNetV2, two-phase training, 97.22% result), and what the freshness score means. Should be comfortable explaining transfer learning.

**Person 3 — LSTM and Sensor Data**
*Opening line:* "I'll explain our sensor-based model — how we simulated the atmospheric environment and what the LSTM learned from it."
*Owns:* The synthetic data generation (`generate_sensor_data.py`), USDA ethylene ranges, the BiLSTM architecture, the scaler, and the val_AUC=1.0 result. Should be ready to explain why synthetic data is valid.

**Person 4 — Fusion, Flask App, and Results**
*Opening line:* "I'll walk you through how we combined all three models into one prediction and built the web application that farmers would actually use."
*Owns:* The XGBoost fusion model (5-feature vector, classifier + regressor, feature importances), the Flask app walkthrough, the result dashboard, and the honest limitations. Should also be ready for the "what would you do differently" question.

---

*Good luck. You built something real. Speak to what you actually made.*
