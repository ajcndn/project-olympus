#!/bin/zsh

# variables
model_name="mistral"
custom_model_name="crewai-mistral"

#get the base model
ollama pull $model_name

#create the model file
ollama create $custom_model_name -f ./MistralModelFile