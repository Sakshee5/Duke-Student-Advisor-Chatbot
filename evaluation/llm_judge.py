import json
import csv
import argparse
import sys
import ollama
import time

def load_qa_pairs(json_path):
    """Load question-answer pairs from a JSON file."""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        sys.exit(1)

def evaluate_qa_pair(question, answer, model_name):
    """Evaluate a single question-answer pair using Ollama."""
    prompt = f"""
    Evaluate the following question-answer pair about Duke University:
    
    Question: {question}
    Answer: {answer}
    
    Please provide the following assessments:
    1. Is this question relevant to Duke University? Answer with 'yes' or 'no'.
    2. On a scale of 1-5 (where 1 is poor and 5 is excellent), rate the clarity of the answer.
    3. Provide general comments on the answer's accuracy, completeness, and helpfulness.
    
    Format your response as a JSON with the following structure:
    {{
        "relevant": "yes/no",
        "clarity": "1-5",
        "comments": "Your comments here"
    }}
    """
    
    # Implement retry logic for API calls
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            response = ollama.chat(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            response_text = response["message"]["content"]
            
            # Extract JSON part
            try:
                # Try to find and parse JSON in the response
                response_text = response_text.strip()
                start_idx = response_text.find("{")
                end_idx = response_text.rfind("}") + 1
                
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = response_text[start_idx:end_idx]
                    result = json.loads(json_str)
                    
                    # Validate the expected fields
                    if "relevant" in result and "clarity" in result and "comments" in result:
                        return result
            except json.JSONDecodeError:
                pass
            
            # If we couldn't parse JSON or it didn't have the expected structure,
            # extract information manually
            result = {}
            
            # Extract relevance (yes/no)
            if "relevant" in response_text.lower():
                if "yes" in response_text.lower() and "no" not in response_text.lower():
                    result["relevant"] = "yes"
                elif "no" in response_text.lower():
                    result["relevant"] = "no"
                else:
                    result["relevant"] = "unclear"
            
            # Extract clarity rating (1-5)
            for i in range(1, 6):
                if f"clarity: {i}" in response_text.lower() or f"clarity rating: {i}" in response_text.lower():
                    result["clarity"] = str(i)
                    break
            if "clarity" not in result:
                result["clarity"] = "3"  # Default
            
            # Extract comments (take everything if we can't find specific comments)
            result["comments"] = response_text[:1000]  # Limit comment size
            
            return result
            
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Attempt {attempt+1} failed. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"Error evaluating Q&A pair: {e}")
                return {
                    "relevant": "unclear",
                    "clarity": "0",
                    "comments": f"Failed to evaluate: {str(e)}"
                }

def main():
    parser = argparse.ArgumentParser(description="Evaluate Duke University Q&A pairs using a local LLM")
    parser.add_argument("input_json", help="Path to JSON file containing Q&A pairs")
    parser.add_argument("output_csv", help="Path for output CSV file")
    parser.add_argument("--model", default="llama3", help="Ollama model to use (default: llama3)")
    args = parser.parse_args()

    print(f"Loading Q&A pairs from {args.input_json}...")
    qa_pairs = load_qa_pairs(args.input_json)
    
    print(f"Using Ollama model: {args.model}")
    results = []
    
    total_pairs = len(qa_pairs)
    for idx, qa_pair in enumerate(qa_pairs):
        question = qa_pair.get("question", "")
        answer = qa_pair.get("answer", "")
        
        print(f"Evaluating pair {idx+1}/{total_pairs}: {question[:50]}...")
        evaluation = evaluate_qa_pair(question, answer, args.model)
        
        results.append({
            "Input Question": question,
            "Input Answer": answer,
            "Relevant Question to Duke university (yes/no)": evaluation.get("relevant", "unclear"),
            "Clarity of answer (1-5)": evaluation.get("clarity", "0"),
            "General Comments": evaluation.get("comments", "")
        })
    
    # Write results to CSV
    with open(args.output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            "Input Question", 
            "Input Answer", 
            "Relevant Question to Duke university (yes/no)", 
            "Clarity of answer (1-5)", 
            "General Comments"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Evaluation complete! Results written to {args.output_csv}")

if __name__ == "__main__":
    main()