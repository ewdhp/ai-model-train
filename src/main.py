import os
from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2LMHeadModel
from datasets import load_dataset, load_from_disk
from gpt2_trainer import GPT2Trainer

# Define functions to download and store the dataset
def download_and_store_dataset(dataset_name, data_dir='./data'):
    # Create the data directory if it doesn't exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Create a subdirectory with the dataset name
    dataset_dir = os.path.join(data_dir, dataset_name.replace('/', '_'))
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir)

    # Load the dataset
    dataset = load_dataset(dataset_name)

    # Save the dataset to the specified directory
    dataset.save_to_disk(dataset_dir)
    print(f"Dataset {dataset_name} downloaded and stored in {dataset_dir}")

    return dataset
def load_local_dataset(dataset_dir):
    # Load the dataset from the specified directory
    dataset = load_from_disk(dataset_dir)
    print(f"Dataset loaded from {dataset_dir}")
    return dataset

# Main function
if __name__ == "__main__":

    # Download and store the dataset
    dataset_name = "prithivMLmods/Deepthink-Reasoning"
    data_dir = "./gpt2-train/data"
    dataset_dir = os.path.join(data_dir, dataset_name.replace('/', '_'))

    # Load the dataset locally
    dataset = load_local_dataset(dataset_dir)

    # Train the model
    print("Training model...")
    trainer = GPT2Trainer()
    trainer.train_manual_grad(dataset)

    # Load the trained model
    print("Loading trained model...")
    tokenizer = GPT2Tokenizer.from_pretrained('./gpt2_tokenizer')
    model = GPT2LMHeadModel.from_pretrained('./gpt2_model')

    # Generate a prompt
    print("Generating prompt...\n\n")
    prompt = "Is 9.11 greater than 9.9?\n\n"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs.input_ids, 
        attention_mask=inputs.attention_mask, 
        max_length=50, 
        num_return_sequences=1)
    
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))