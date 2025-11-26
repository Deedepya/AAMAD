//
//  DocumentCaptureView.swift
//  OnboardingiOSApp
//
//  Created by @frontend.eng
//

import SwiftUI
import AVFoundation

/// Upload status enumeration
enum UploadStatus {
    case idle
    case uploading
    case success
    case error
}

/// View for capturing documents using the camera
struct DocumentCaptureView: View {
    @Binding var selectedDocumentType: DocumentType?
    @Binding var capturedImage: UIImage?
    @Environment(\.dismiss) var dismiss
    @State private var showCamera = false
    @State private var cameraPermissionStatus: AVAuthorizationStatus = .notDetermined
    
    var body: some View {
        NavigationView {
            ZStack {
                Color(.systemBackground)
                    .ignoresSafeArea()
                
                VStack(spacing: 24) {
                    // Document type selection
                    if selectedDocumentType == nil {
                        documentTypeSelectionView
                    } else {
                        // Camera interface
                        cameraInterfaceView
                    }
                }
                .padding()
            }
            .navigationTitle("Capture Document")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .navigationBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                }
            }
            .sheet(isPresented: $showCamera) {
                CameraView(image: $capturedImage)
            }
            .onAppear {
                checkCameraPermission()
            }
        }
    }
    
    // MARK: - Document Type Selection
    
    private var documentTypeSelectionView: some View {
        VStack(spacing: 20) {
            Text("Select Document Type")
                .font(.title2)
                .fontWeight(.semibold)
                .padding(.top)
            
            ForEach(DocumentType.allCases, id: \.self) { type in
                Button(action: {
                    selectedDocumentType = type
                }) {
                    HStack {
                        Image(systemName: iconForDocumentType(type))
                            .font(.title2)
                            .foregroundColor(.blue)
                            .frame(width: 44, height: 44)
                        
                        Text(type.rawValue)
                            .font(.body)
                            .foregroundColor(.primary)
                        
                        Spacer()
                        
                        Image(systemName: "chevron.right")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                    .padding()
                    .background(Color(.systemGray6))
                    .cornerRadius(12)
                }
                .buttonStyle(PlainButtonStyle())
            }
        }
    }
    
    // MARK: - Camera Interface
    
    private var cameraInterfaceView: some View {
        VStack(spacing: 20) {
            // Instructions
            VStack(spacing: 8) {
                Text("Position your \(selectedDocumentType?.rawValue ?? "document")")
                    .font(.headline)
                
                Text("Ensure the document is flat, well-lit, and fully visible in the frame")
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }
            .padding()
            
            // Alignment guide overlay placeholder
            ZStack {
                RoundedRectangle(cornerRadius: 12)
                    .stroke(Color.blue, lineWidth: 2)
                    .frame(width: 300, height: 200)
                
                VStack {
                    Spacer()
                    Text("Document Frame")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    Spacer()
                }
            }
            .frame(height: 300)
            .background(Color(.systemGray6))
            .cornerRadius(12)
            
            // Action buttons
            HStack(spacing: 16) {
                Button(action: {
                    selectedDocumentType = nil
                }) {
                    Text("Change Type")
                        .font(.body)
                        .foregroundColor(.blue)
                        .padding(.horizontal, 20)
                        .padding(.vertical, 12)
                        .background(Color(.systemGray6))
                        .cornerRadius(12)
                }
                
                Button(action: {
                    requestCameraPermission()
                }) {
                    HStack {
                        Image(systemName: "camera.fill")
                        Text("Capture")
                    }
                    .font(.body)
                    .fontWeight(.semibold)
                    .foregroundColor(.white)
                    .padding(.horizontal, 32)
                    .padding(.vertical, 12)
                    .background(cameraPermissionStatus == .authorized ? Color.blue : Color.gray)
                    .cornerRadius(12)
                }
                .disabled(cameraPermissionStatus != .authorized)
            }
            .padding(.top)
        }
    }
    
    // MARK: - Helper Methods
    
    private func iconForDocumentType(_ type: DocumentType) -> String {
        switch type {
        case .i9:
            return "doc.text.fill"
        case .w4:
            return "doc.text.fill"
        case .driversLicense:
            return "creditcard.fill"
        case .passport:
            return "book.fill"
        case .socialSecurityCard:
            return "person.text.rectangle.fill"
        }
    }
    
    private func checkCameraPermission() {
        cameraPermissionStatus = AVCaptureDevice.authorizationStatus(for: .video)
    }
    
    private func requestCameraPermission() {
        AVCaptureDevice.requestAccess(for: .video) { granted in
            DispatchQueue.main.async {
                if granted {
                    cameraPermissionStatus = .authorized
                    showCamera = true
                } else {
                    cameraPermissionStatus = .denied
                }
            }
        }
    }
}

// MARK: - Camera View

struct CameraView: UIViewControllerRepresentable {
    @Binding var image: UIImage?
    @Environment(\.dismiss) var dismiss
    
    func makeUIViewController(context: Context) -> UIImagePickerController {
        let picker = UIImagePickerController()
        picker.sourceType = .camera
        picker.delegate = context.coordinator
        picker.allowsEditing = false
        return picker
    }
    
    func updateUIViewController(_ uiViewController: UIImagePickerController, context: Context) {}
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject, UIImagePickerControllerDelegate, UINavigationControllerDelegate {
        let parent: CameraView
        
        init(_ parent: CameraView) {
            self.parent = parent
        }
        
        func imagePickerController(_ picker: UIImagePickerController, didFinishPickingMediaWithInfo info: [UIImagePickerController.InfoKey : Any]) {
            if let image = info[.originalImage] as? UIImage {
                parent.image = image
            }
            parent.dismiss()
        }
        
        func imagePickerControllerDidCancel(_ picker: UIImagePickerController) {
            parent.dismiss()
        }
    }
}

// MARK: - Preview

struct DocumentCaptureView_Previews: PreviewProvider {
    static var previews: some View {
        DocumentCaptureView(
            selectedDocumentType: .constant(.i9),
            capturedImage: .constant(nil)
        )
    }
}
